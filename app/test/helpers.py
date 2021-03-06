import json
from app.main import db
from app.main.model.user import User
from app.main.model.group import Group
from app.main.service.group_service import get_a_group_by_id
import datetime


def create_group(self):
    group = Group(
        name='adminGroup',
        description='A group for bootstrapping testing',
        public_id='123456'
    )
    db.session.add(group)
    db.session.commit()

    return group


def create_admin_user(self, group=False):
    if not group:
        group = create_group(self)

    user = User(
        username='admin',
        email='admin@example.com',
        password='admin',
        group_id=group.id,
        admin=True,
        public_id='1',
        registered_on=datetime.datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return {
        'user': user,
        'group': group,
        'authKey': User.encode_auth_token(user.id)
    }


def create_nonadmin_user(self, groupId=False):
    if groupId:
        group = Group.query.filter_by(id=groupId).first()
    else:
        group = create_group(self)
        groupId = group.id

    user = User(
        username='steve',
        email='steve@steve.com',
        password='steve',
        group_id=groupId,
        public_id='12342134',
        admin=False,
        registered_on=datetime.datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return {
        'user': user,
        'group': group,
        'authKey': User.encode_auth_token(user.id)
    }


def get_nonadmin_authKey(self):
    create_nonadmin_user(self)
    # registered user login
    loginResponse = self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='steve@steve.com',
            password='steve'
        )),
        content_type='application/json'
    )
    return json.loads(loginResponse.data.decode())['Authorization']


def get_admin_authKey(self):
    create_admin_user(self)
    # registered user login
    loginResponse = self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='admin@example.com',
            password='admin'
        )),
        content_type='application/json'
    )
    return json.loads(loginResponse.data.decode())['Authorization']


def create_log_entry(self, authKey, subject, text):
    return self.client.post(
        '/api/entry/',
        headers=dict(
            Authorization=authKey
        ),
        data=json.dumps(dict(
            subject=subject,
            text=text,
            group_name="adminGroup"
        )),
        content_type='application/json'
    )
