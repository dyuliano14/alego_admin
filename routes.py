from flask import render_template
from alego_admin import app


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')
