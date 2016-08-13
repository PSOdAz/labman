from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from .member import Member


mod_profile = Blueprint('mod_profile', __name__, static_folder='../static', url_prefix='/profile')


@mod_profile.route('/', methods=['GET', 'POST'])
def display():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_member_by_uid(session['uid'])
    if request.method == 'GET':
        supervisors = Member.list_supervisors()
        return render_template('profile.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if member.update(request.form):
            flash('Profile updated!')
        else:
            flash('Failed to update your profile!')
        return redirect(url_for('mod_admin.overview'))


@mod_profile.route('/publications', methods=['POST', 'DELETE'])
def publications():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_member_by_uid(session['uid'])
    if request.method == 'POST':
        member.add_publication(request.form['new_pub'])
        return redirect(url_for('mod_profile.display'))
    else:
        pass


@mod_profile.route('/avatar', methods=['POST'])
def avatar():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_member_by_uid(session['uid'])
    if 'file' in request.files:
        url = member.change_avatar(request.files['file'])
        return jsonify({'avatar_url': url})
