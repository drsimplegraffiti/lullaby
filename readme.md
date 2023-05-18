##### Setup using pipenv

Check python version
> python --version -> Python 3.10.11

> pipenv --python 3.10.11


---

#### Activate pipenv
> pipenv shell

---

#### EXIT pipenv
> exit OR run: deactivate


--- 

#### Install dependencies
> pipenv install flask flask_sqlalchemy flask_jwt_extended mysqlclient


```sql
  create table users(
  id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    profile_image BLOB,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_code VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    user_role VARCHAR(255) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )

    
```

Add profile_image as blob to users table
```sql
ALTER TABLE users ADD profile_image BLOB;
```

Add is_verified, verification_code, is_active, user_role to users table
```sql
ALTER TABLE users ADD is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD verification_code VARCHAR(255);
ALTER TABLE users ADD is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD user_role VARCHAR(255) DEFAULT 'user';
```