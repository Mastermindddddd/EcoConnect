"""
Flask admin route to scrape PETCO Buy-Back Centres, geocode with Google Maps API,
and insert/update into your RecyclingCenter model.

Usage:
1. Put this file in your Flask app (e.g. src/seed/seed_petco_centres.py) and import/register
   the blueprint with your app.
2. Configure environment variables or app.config:
   - GOOGLE_MAPS_API_KEY  : your Google Maps Geocoding API key
   - ADMIN_SEED_TOKEN     : a secret token used to protect the endpoint
3. Call the endpoint (POST) with header `X-ADMIN-TOKEN: <ADMIN_SEED_TOKEN>` to run.

Notes:
- This scrapes data from PETCO's public "Buy Back Centres" page. Verify terms of reuse
  if you plan to redistribute or commercialize the data.
- Geocoding uses Google Maps API (paid/usage limits may apply).

"""

from flask import Blueprint, current_app, request, jsonify
from bs4 import BeautifulSoup
import requests
import time
import urllib.parse
import os
import json

# Import your application models and db
# Adjust these imports to match your project layout
from src.models.user import db
from src.models.recycling_center import RecyclingCenter

seed_bp = Blueprint('seed_petco', __name__)

PETCO_URL = "https://petco.co.za/buy-back-centres/"


def geocode_address(address, api_key):
    """Return (lat, lng) or (None, None) on failure."""
    if not api_key:
        return None, None
    encoded = urllib.parse.quote_plus(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded}&key={api_key}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get('status') == 'OK' and data.get('results'):
            loc = data['results'][0]['geometry']['location']
            return float(loc['lat']), float(loc['lng'])
        else:
            current_app.logger.debug('Geocode failed for %s: %s', address, data.get('status'))
            return None, None
    except Exception as e:
        current_app.logger.exception('Geocoding error for %s', address)
        return None, None


@seed_bp.route('/admin/seed-centres', methods=['POST'])
def seed_petco_centres():
    """Scrape PETCO buy-back centres and insert/update into DB without geocoding."""
    ADMIN_TOKEN = current_app.config.get('ADMIN_SEED_TOKEN') or os.getenv('ADMIN_SEED_TOKEN')
    provided = request.headers.get('X-ADMIN-TOKEN')
    if not ADMIN_TOKEN or provided != ADMIN_TOKEN:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    summary = {'created': 0, 'updated': 0, 'skipped': 0, 'failed': []}

    try:
        resp = requests.get(PETCO_URL, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to fetch PETCO page: {e}'}), 500

    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    if not table:
        rows = soup.find_all('tr')
    else:
        rows = table.find_all('tr')

    entries = []
    for i, tr in enumerate(rows):
        cols = tr.find_all(['td', 'th'])
        if i == 0 and any('name' in (c.get_text('').lower()) for c in cols):
            continue
        if len(cols) < 3:
            continue

        text_cols = [c.get_text(strip=True) for c in cols]
        while len(text_cols) < 6:
            text_cols.append('')

        entry = {
            'name': text_cols[0],
            'area': text_cols[1],
            'town': text_cols[2],
            'contact': text_cols[3] if len(text_cols) > 3 else '',
            'phone': text_cols[4] if len(text_cols) > 4 else '',
            'email': text_cols[5] if len(text_cols) > 5 else '',
        }
        if entry['name']:
            entries.append(entry)

    unique = {}
    for e in entries:
        key = (e['name'].lower(), e['town'].lower())
        if key not in unique:
            unique[key] = e

    for key, e in unique.items():
        try:
            existing = RecyclingCenter.query.filter(
                RecyclingCenter.name.ilike(e['name']),
                RecyclingCenter.address.ilike(f"%{e['town']}%")
            ).first()

            if existing:
                existing.phone = e.get('phone') or existing.phone
                existing.email = e.get('email') or existing.email
                existing.special_instructions = existing.special_instructions or e.get('contact')
                existing.is_active = True
                db.session.add(existing)
                summary['updated'] += 1
            else:
                rc = RecyclingCenter(
                    name=e.get('name'),
                    address=e.get('area') + ', ' + e.get('town') if e.get('area') else e.get('town'),
                    latitude=None,   # No geocoding
                    longitude=None,  # No geocoding
                    phone=e.get('phone') or None,
                    email=e.get('email') or None,
                    website=None,
                    operating_hours=json.dumps({}),
                    accepted_materials=json.dumps([]),
                    special_instructions=e.get('contact') or None,
                    is_active=True
                )
                db.session.add(rc)
                summary['created'] += 1

        except Exception as exc:
            current_app.logger.exception('Failed to insert/update centre: %s', e)
            summary['failed'].append({'entry': e, 'error': str(exc)})
            try:
                db.session.rollback()
            except Exception:
                pass

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.exception('Commit failed')
        db.session.rollback()
        return jsonify({'success': False, 'error': 'DB commit failed', 'details': str(e)}), 500

    return jsonify({'success': True, 'summary': summary, 'imported': summary['created'] + summary['updated']})
