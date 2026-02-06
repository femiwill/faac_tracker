import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'faac-tracker-dev-key-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///faac.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

db = SQLAlchemy(app)


# ── Models ──────────────────────────────────────────────────────────────────

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    geo_zone = db.Column(db.String(50), nullable=False)
    lgas = db.relationship('LGA', backref='state', lazy=True)
    allocations = db.relationship('FAACAllocation', backref='state', lazy=True)
    igr_records = db.relationship('IGR', backref='state', lazy=True)


class LGA(db.Model):
    __tablename__ = 'lgas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    allocations = db.relationship('FAACAllocation', backref='lga', lazy=True)


class FAACAllocation(db.Model):
    __tablename__ = 'faac_allocations'
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    lga_id = db.Column(db.Integer, db.ForeignKey('lgas.id'), nullable=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    statutory_allocation = db.Column(db.Float, default=0)
    vat_allocation = db.Column(db.Float, default=0)
    total_gross = db.Column(db.Float, default=0)
    deductions = db.Column(db.Float, default=0)
    net_allocation = db.Column(db.Float, default=0)


class IGR(db.Model):
    __tablename__ = 'igr'
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, default=0)


# ── Helpers ─────────────────────────────────────────────────────────────────

MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

GEO_ZONES = [
    'North Central', 'North East', 'North West',
    'South East', 'South South', 'South West'
]


def fmt_naira(amount):
    """Format amount in billions/millions for display."""
    if amount is None:
        return '₦0'
    if amount >= 1_000_000_000:
        return f'₦{amount / 1_000_000_000:,.2f}B'
    if amount >= 1_000_000:
        return f'₦{amount / 1_000_000:,.2f}M'
    return f'₦{amount:,.0f}'


app.jinja_env.filters['naira'] = fmt_naira
app.jinja_env.globals['MONTH_NAMES'] = MONTH_NAMES
app.jinja_env.globals['GEO_ZONES'] = GEO_ZONES


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    states = State.query.order_by(State.name).all()

    # Latest month summary
    latest = db.session.query(
        FAACAllocation.year, FAACAllocation.month
    ).filter(
        FAACAllocation.lga_id.is_(None)
    ).order_by(
        FAACAllocation.year.desc(), FAACAllocation.month.desc()
    ).first()

    summary = []
    if latest:
        top_states = FAACAllocation.query.filter_by(
            year=latest.year, month=latest.month, lga_id=None
        ).order_by(FAACAllocation.net_allocation.desc()).limit(5).all()
        summary = top_states

    zones = {}
    for s in states:
        zones.setdefault(s.geo_zone, []).append(s)

    return render_template('index.html',
                           states=states, zones=zones,
                           summary=summary, latest=latest)


@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])

    results = []
    states = State.query.filter(State.name.ilike(f'%{q}%')).limit(5).all()
    for s in states:
        results.append({'type': 'state', 'name': s.name, 'url': url_for('state_detail', name=s.name)})

    lgas = LGA.query.filter(LGA.name.ilike(f'%{q}%')).limit(5).all()
    for lg in lgas:
        results.append({'type': 'lga', 'name': f'{lg.name} ({lg.state.name})',
                        'url': url_for('lga_detail', state_name=lg.state.name, lga_name=lg.name)})

    return jsonify(results)


@app.route('/state/<name>')
def state_detail(name):
    state = State.query.filter(State.name.ilike(name)).first_or_404()

    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    alloc_query = FAACAllocation.query.filter_by(state_id=state.id, lga_id=None)
    if year:
        alloc_query = alloc_query.filter_by(year=year)
    if month:
        alloc_query = alloc_query.filter_by(month=month)

    allocations = alloc_query.order_by(
        FAACAllocation.year.desc(), FAACAllocation.month.desc()
    ).all()

    igr_data = IGR.query.filter_by(state_id=state.id).order_by(IGR.year.desc(), IGR.quarter).all()

    lga_allocations = []
    latest = db.session.query(
        FAACAllocation.year, FAACAllocation.month
    ).filter(
        FAACAllocation.state_id == state.id, FAACAllocation.lga_id.isnot(None)
    ).order_by(
        FAACAllocation.year.desc(), FAACAllocation.month.desc()
    ).first()

    if latest:
        lga_allocations = FAACAllocation.query.filter(
            FAACAllocation.state_id == state.id,
            FAACAllocation.lga_id.isnot(None),
            FAACAllocation.year == latest.year,
            FAACAllocation.month == latest.month
        ).order_by(FAACAllocation.net_allocation.desc()).all()

    available_years = db.session.query(FAACAllocation.year).filter_by(
        state_id=state.id, lga_id=None
    ).distinct().order_by(FAACAllocation.year.desc()).all()
    available_years = [y[0] for y in available_years]

    # Chart data
    chart_labels = [f"{MONTH_NAMES[a.month][:3]} {a.year}" for a in reversed(allocations)]
    chart_statutory = [a.statutory_allocation for a in reversed(allocations)]
    chart_vat = [a.vat_allocation for a in reversed(allocations)]
    chart_net = [a.net_allocation for a in reversed(allocations)]

    return render_template('state.html',
                           state=state, allocations=allocations,
                           igr_data=igr_data, lga_allocations=lga_allocations,
                           latest_lga=latest,
                           available_years=available_years,
                           filter_year=year, filter_month=month,
                           chart_labels=chart_labels,
                           chart_statutory=chart_statutory,
                           chart_vat=chart_vat,
                           chart_net=chart_net)


@app.route('/lga/<state_name>/<lga_name>')
def lga_detail(state_name, lga_name):
    state = State.query.filter(State.name.ilike(state_name)).first_or_404()
    lga = LGA.query.filter(LGA.name.ilike(lga_name), LGA.state_id == state.id).first_or_404()

    allocations = FAACAllocation.query.filter_by(lga_id=lga.id).order_by(
        FAACAllocation.year.desc(), FAACAllocation.month.desc()
    ).all()

    chart_labels = [f"{MONTH_NAMES[a.month][:3]} {a.year}" for a in reversed(allocations)]
    chart_net = [a.net_allocation for a in reversed(allocations)]

    return render_template('lga.html', state=state, lga=lga,
                           allocations=allocations,
                           chart_labels=chart_labels,
                           chart_net=chart_net)


@app.route('/compare', methods=['GET'])
def compare():
    states = State.query.order_by(State.name).all()
    selected_names = request.args.getlist('states')

    compared = []
    for name in selected_names[:3]:
        s = State.query.filter(State.name.ilike(name)).first()
        if s:
            allocs = FAACAllocation.query.filter_by(
                state_id=s.id, lga_id=None
            ).order_by(FAACAllocation.year, FAACAllocation.month).all()

            igr_total = db.session.query(db.func.sum(IGR.amount)).filter_by(
                state_id=s.id
            ).scalar() or 0

            compared.append({
                'state': s,
                'allocations': allocs,
                'igr_total': igr_total,
                'labels': [f"{MONTH_NAMES[a.month][:3]} {a.year}" for a in allocs],
                'net_values': [a.net_allocation for a in allocs],
            })

    return render_template('compare.html', states=states, compared=compared,
                           selected_names=selected_names)


# ── Admin ───────────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == app.config['ADMIN_PASSWORD']:
            session['admin'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Incorrect password.', 'danger')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin_dashboard():
    states = State.query.order_by(State.name).all()
    return render_template('admin.html', states=states)


@app.route('/admin/add_allocation', methods=['POST'])
@login_required
def admin_add_allocation():
    state_id = request.form.get('state_id', type=int)
    month = request.form.get('month', type=int)
    year = request.form.get('year', type=int)
    statutory = request.form.get('statutory_allocation', type=float, default=0)
    vat = request.form.get('vat_allocation', type=float, default=0)
    deductions = request.form.get('deductions', type=float, default=0)
    total_gross = statutory + vat
    net = total_gross - deductions

    existing = FAACAllocation.query.filter_by(
        state_id=state_id, lga_id=None, month=month, year=year
    ).first()

    if existing:
        existing.statutory_allocation = statutory
        existing.vat_allocation = vat
        existing.total_gross = total_gross
        existing.deductions = deductions
        existing.net_allocation = net
        flash('Allocation updated.', 'success')
    else:
        alloc = FAACAllocation(
            state_id=state_id, lga_id=None, month=month, year=year,
            statutory_allocation=statutory, vat_allocation=vat,
            total_gross=total_gross, deductions=deductions, net_allocation=net
        )
        db.session.add(alloc)
        flash('Allocation added.', 'success')

    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/api/lgas/<int:state_id>')
def api_lgas(state_id):
    lgas = LGA.query.filter_by(state_id=state_id).order_by(LGA.name).all()
    return jsonify([{'id': lg.id, 'name': lg.name} for lg in lgas])


# ── Init ────────────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
