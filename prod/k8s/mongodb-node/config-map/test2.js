const targetDbStr = 'test';
const rootUser = 'admin';
const rootPass = 'admin';
// const usersStr = cat('/etc/k8-test/MONGO_USERS_LIST');
const adminDb = db.getSiblingDB('admin');
adminDb.auth(rootUser, rootPass);
print('Successfully authenticated admin user');
const targetDb = db.getSiblingDB(targetDbStr);
const customRoles = adminDb
  .getRoles({rolesInfo: 1, showBuiltinRoles: false})
  .map(role =&gt; role.role)
  .filter(Boolean);
usersStr
  .trim()
  .split(';')
  .map(s =&gt; s.split(':'))
  .forEach(user =&gt; {
    const username = user[0];
    const rolesStr = user[1];
    const password = user[2];
    if (!rolesStr || !password) {
      return;
    }
    const roles = rolesStr.split(',');
    const userDoc = {
      user: username,
      pwd: password,
    };
    userDoc.roles = roles.map(role =&gt; {
      if (!~customRoles.indexOf(role)) {
        return role;
      }
      return {role: role, db: 'admin'};
    });
    try {
      targetDb.createUser(userDoc);
    } catch (err) {
      if (!~err.message.toLowerCase().indexOf('duplicate')) {
        throw err;
      }
    }
  });