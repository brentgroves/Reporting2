const adminDb = db.getSiblingDB('admin');
adminDb.createUser({user: "sysadmin", pwd: "password123", roles:["root"]});