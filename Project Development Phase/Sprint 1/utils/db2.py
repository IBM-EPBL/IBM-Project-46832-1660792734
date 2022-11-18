import ibm_db

# IBM DB2 Credentials
# DATABASE=<databasename>;HOSTNAME=<your-hostname>;PORT=<portnumber>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=<username>;PWD=<password>

from keys import DB2_URL

conn = ibm_db.connect(DB2_URL,'','')
