from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'amana-secret-2026'

def get_db():
    conn = sqlite3.connect('amana.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Waitlist table
    c.execute('''
        CREATE TABLE IF NOT EXISTS waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            location TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Auctions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bond_number TEXT NOT NULL,
            tenor_years INTEGER NOT NULL,
            coupon_rate REAL NOT NULL,
            auction_date TEXT NOT NULL,
            maturity_date TEXT NOT NULL,
            min_investment INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'upcoming',
            amount_offered TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            message TEXT NOT NULL,
            read INTEGER DEFAULT 0,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed with real past auctions if empty
    c.execute('SELECT COUNT(*) FROM auctions')
    if c.fetchone()[0] == 0:
        auctions = [
            ('700', 5, 10.25, '2026-04-29', '2031-04-29', 1000000, 'closed', 'TZS 124 Bilioni'),
            ('699', 10, 10.50, '2026-04-15', '2036-04-15', 1000000, 'closed', 'TZS 152 Bilioni'),
            ('698', 20, 12.00, '2026-03-18', '2046-03-18', 1000000, 'closed', 'TZS 200 Bilioni'),
            ('701', 15, 10.75, '2026-05-13', '2041-05-14', 1000000, 'closed', 'TZS 124 Bilioni'),
        ]
        c.executemany('''
            INSERT INTO auctions 
            (bond_number, tenor_years, coupon_rate, auction_date, maturity_date, min_investment, status, amount_offered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', auctions)

    conn.commit()
    conn.close()

# ─── PUBLIC ROUTES ───────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jifunze')
def jifunze():
    conn = get_db()
    auctions = conn.execute('''
        SELECT * FROM auctions 
        ORDER BY auction_date DESC
    ''').fetchall()
    conn.close()
    return render_template('jifunze.html', auctions=auctions)

# ─── WAITLIST ─────────────────────────────────────────────

@app.route('/join', methods=['POST'])
def join():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    location = data.get('location', '').strip()

    if not name or not phone:
        return jsonify({'success': False, 'message': 'Jina na namba ya simu inahitajika.'})

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM waitlist WHERE phone = ?', (phone,))
    if c.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Namba hii imeshasajiliwa.'})

    c.execute('INSERT INTO waitlist (name, email, phone, location) VALUES (?, ?, ?, ?)',
              (name, email, phone, location))
    conn.commit()

    c.execute('SELECT COUNT(*) FROM waitlist')
    count = c.fetchone()[0]
    conn.close()

    return jsonify({
        'success': True,
        'message': f'Umefanikiwa! Unashika nafasi namba {count}.',
        'count': count
    })

@app.route('/count')
def count():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM waitlist')
    count = c.fetchone()[0]
    conn.close()
    return jsonify({'count': count})


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name', '').strip()
    message = data.get('message', '').strip()
    phone = data.get('phone', '').strip()

    if not name or not message:
        return jsonify({'success': False, 'message': 'Jina na ujumbe vinahitajika.'})

    conn = get_db()

    conn.execute('INSERT INTO messages (name, phone, message) VALUES (?, ?, ?)',
                 (name, phone, message))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Ujumbe wako umepokelewa. Tutawasiliana nawe hivi karibuni.'})

# ─── ADMIN ───────────────────────────────────────────────-

ADMIN_PASSWORD = 'amana2026'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and 'password' in request.form:
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
        else:
            return render_template('admin.html', error='Nywila si sahihi.', logged_in=False)

    if not session.get('admin'):
        return render_template('admin.html', logged_in=False)

    conn = get_db()
    auctions = conn.execute('SELECT * FROM auctions ORDER BY auction_date DESC').fetchall()
    waitlist = conn.execute('SELECT * FROM waitlist ORDER BY joined_at DESC').fetchall()
    messages = conn.execute('SELECT * FROM messages ORDER BY sent_at DESC').fetchall()
    unread = conn.execute('SELECT COUNT(*) as c FROM messages WHERE read = 0').fetchone()['c']
    count = conn.execute('SELECT COUNT(*) as c FROM waitlist').fetchone()['c']
    conn.close()

    return render_template('admin.html', 
                     logged_in=True, 
                     auctions=auctions,
                     waitlist=waitlist,
                     count=count,
                     messages=messages,
                     unread=unread)

@app.route('/admin/auction/add', methods=['POST'])
def add_auction():
    if not session.get('admin'):
        return redirect('/admin')
    
    conn = get_db()
    conn.execute('''
        INSERT INTO auctions 
        (bond_number, tenor_years, coupon_rate, auction_date, maturity_date, min_investment, status, amount_offered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        request.form['bond_number'],
        int(request.form['tenor_years']),
        float(request.form['coupon_rate']),
        request.form['auction_date'],
        request.form['maturity_date'],
        int(request.form['min_investment']),
        request.form['status'],
        request.form['amount_offered']
    ))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin/auction/delete/<int:id>')
def delete_auction(id):
    if not session.get('admin'):
        return redirect('/admin')
    conn = get_db()
    conn.execute('DELETE FROM auctions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)