import sqlite3

class Sqlite:
	'Common stuff for sqlite class'
	dbExists = False
	conn = False

	def __init__(self):
		if Sqlite.checkDBExist():
			Sqlite.dbExists = True
			Sqlite.conn = sqlite3.connect('sync.db')
		else:
			return False

		return True

	@staticmethod
	def checkDBExist(self):
		return 1

	def buildDatabase(self):

		#create files and folders table
		sqlCreateFilesTable = """CREATE TABLE files_n_folders (
																FILEID BIGINT NOT NULL,
																FILENAME TEXT NOT NULL,
																FILESIZE INTEGER NOT NULL,
																CREATIONTIME TEXT NOT NULL,
																LASTMODIFIED TEXT NOT NULL,
																FILEPATH TEXT NOT NULL,
																ISFOLDER INTEGER NOT NULL DEFAULT (0)
																)"""
		Sqlite.conn.execute(sqlCreateFilesTable)

		#create files and folders mapping
		sqlCreateFileMap = """CREATE TABLE `FILE_MAP` (
														`FOLDER_FILEID`	INTEGER NOT NULL,
														`FILE_FILEID`	INTEGER NOT NULL UNIQUE,
														PRIMARY KEY(FILE_FILEID)
														)"""
		Sqlite.conn.execute(sqlCreateFileMap)

		#create peer to file mapping
		sqlCreatePeerTable = """CREATE TABLE `PEER_FILE` (
															`PEERID`	INTEGER NOT NULL,
															`FILEID`	INTEGER NOT NULL
															)"""
		Sqlite.conn.execute(sqlCreatePeerTable)

		#create peer info table
		sqlPeerTable = """CREATE TABLE `PEERS` (
													`PEERID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
													`MACADD`	INTEGER NOT NULL,
													`STATUS`	INTEGER,
													`LASTCONNECTED`	TEXT,
													`UPTIME`	INTEGER NOT NULL
												)"""
		Sqlite.conn.execute(sqlPeerTable)

        #create peer file table
        sqlPeerFile = """CREATE TABLE `PEER_FILE` (
	                                                `PEERID`	INTEGER NOT NULL,
	                                                `FILEID`	INTEGER NOT NULL
                                                    )"""
        Sqlite.conn.execute(sqlPeerFile)
        return

	def selectSQL(self):
		t = ('RHAT',)
		Sqlite.conn.execute('SELECT * FROM stocks WHERE symbol=?', t)
		print Sqlite.conn.fetchone()

	def insertSQL(sqlCommand):
		purchases = 	[
				('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
				('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
						('2006-04-06', 'SELL', 'IBM', 500, 53.00),
						]
		Sqlite.conn.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

	def removeSQL(self):
        print 'remove sql'
        return

	def updateSQL(self):
        print 'update sql'
        return

