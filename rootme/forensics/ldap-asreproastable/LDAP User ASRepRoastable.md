#### Statement

During your investigations, you found a backup of the company’s LDAP made with [ldap2json](https://github.com/p0dalirius/ldap2json). Use the information in this file to find the ASRepRoastable user.

The flag is the email address of the ASRepRoastable user.

This challenge is similar to the one "KerbeRoastable" I solved a few months ago. 

The docs that are being given in this challenge : https://en.hackndo.com/kerberos-asrep-roasting/

## Kerberos : Pre-auth

In Kerberos first exchange : (KRB_AS_REQ - KRB_AS_REP)
the client must first authenticate himself to the domain controller, before obtaining a TGT. 

A part of the response of the domain controller being encrypted with the client’s account secret (the session key), it is important that this information is not accessible without authentication. 
Otherwise, anyone could ask for a TGT for a given account, and try to decrypt the encrypted part of the response KRB_AS_REP in a brute-force way in order to recover the password of the targeted user.

That’s why the user, in his KRB_AS_REQ request, must send an authenticator encrypted with his own secret in order for the domain controller to decrypt it and send back the KRB_AS_REP if it is successful. 

If an attacker asks for a TGT with an account he does not have control over, he won’t be able to encrypt the authenticator correctly, therefore the domain controller will not return the desired information.

## KRB_AS_REP Roasting

However, it is possible to disable the pre-authentication for one or more accounts.

If this option is disabled, anyone could ask for a TGT in the name of one of these accounts, without sending any authenticator, and the domain controller will send back a KRB_AS_REP.

## Finding the account

While analyzing the ch32.json file, we identified a user account with a value of 4260352 for the userAccountControl attribute. By breaking down this bitmask according to Active Directory specifications, we get: 
512 (NORMAL_ACCOUNT) 
65536 (DONT_EXPIRE_PASSWORD) 
4194304 (DONT_REQ_PREAUTH)
The presence of the DONT_REQ_PREAUTH flag (bit 0x400000) categorically confirms that this account is vulnerable to an AS-REP Roasting attack. It was from this same JSON object block that we were able to extract the associated email address to validate the challenge flag.

Here is an extract of the JSON for this user. 

The goal is to simply extract the corresponding e-mail address.
```json
"name": "Fitzgerald", "objectGUID": "{f3c1fa29-268a-4092-b183-bbe6c837ad79}", "userAccountControl": 4260352, "badPwdCount": 0, "codePage": 0, "countryCode": 0, "badPasswordTime": "1601-01-01 00:00:00", "lastLogoff": "1601-01-01 00:00:00", "lastLogon": "1601-01-01 00:00:00", "pwdLastSet": "2022-08-30 03:44:38", "primaryGroupID": 513, "objectSid": "S-1-5-21-1356747155-1897123353-4258384033-2027", "accountExpires": "9999-12-31 23:59:59", "logonCount": 0, "sAMAccountName": "flandry", "sAMAccountType": 805306368, "objectCategory": "CN=Person,CN=Schema,CN=Configuration,DC=ROOTME,DC=local", "dSCorePropagationData": ["1601-01-01 00:00:00"], "msDS-SupportedEncryptionTypes": 0, "mail": "fitzgerald.landry@rootme.local"},
``` 
