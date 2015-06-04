/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.dao;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import syncfiles.dao.db.DBConnManager;
import syncfiles.filesystem.FileIndexThread;

/**
 *
 * @author Gabriel
 */
public class DAOFiles {

    /**
     * Check if file or folder already exists in database. This function check
     * if file or folder is already indexed in database returning true or false.
     * <p>
     *
     * @param filePath string containing the path to a file or folder
     * @return true if file does exist or false if it does not
     * @see DAOFiles
     */
    private synchronized static boolean checkFileExistance(String filePath) {
        DBConnManager.initializeDatabaseConnection();
        
              MessageDigest m = null;
            try
            {
                m = MessageDigest.getInstance("MD5");
            } catch (NoSuchAlgorithmException ex) 
            {
                Logger.getLogger(DAOFiles.class.getName()).log(Level.SEVERE, null, ex);
            }
            if (m != null)
            {
                m.update(filePath.getBytes(), 0, filePath.length());
            }
        
        //Cria select, futuramente em DAOFiles
        String sql = "SELECT * FROM files_n_folders "
                + "WHERE files_n_folders.fileid= '" + new BigInteger(1, m.digest()).toString(16)  + "';";

        //Roda query
        ResultSet rs = DBConnManager.runQueryAndReturn(sql);
        if (rs != null) {
            //Query retornou com sucesso
            try {
                //Checa se arquivo existe
                if (rs.next() == true) {
                    //File exists
                    return true;
                }
            } catch (SQLException ex) {
                Logger.getLogger(FileIndexThread.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        return false;
    }

    /**
     * Insert new file or folder to the database. This function check if file or
     * folder is already indexed in database and if it is not indexed yet, try
     * to insert it to the database.
     * <p>
     *
     * @param fileName string containing the file or folder name
     * @param fileSize file size in bytes
     * @param creationTime timestamp of file creation
     * @param lastModified timestamp of last file modification
     * @param filePath string containing the entire path to the file
     * @param isFolder boolean value indicating that the file is really a file,
     * or a folder
     *
     * @return true if file was inserted or already exists, or not if any of
     * those failed
     *
     * @see DAOFiles
     */
    public synchronized static boolean insertNewFile(String fileName, long fileSize, String creationTime, String lastModified, String filePath, boolean isFolder) {
        if (checkFileExistance(filePath) != true) {
            MessageDigest m = null;
            try {
                m = MessageDigest.getInstance("MD5");
            } catch (NoSuchAlgorithmException ex) {
                Logger.getLogger(DAOFiles.class.getName()).log(Level.SEVERE, null, ex);
            }
            if (m != null) {
                m.update(filePath.getBytes(), 0, filePath.length());
                String sql = "INSERT INTO files_n_folders (fileid, filename, filesize, creationtime, lastmodified, filepath, isfolder)"
                        + " VALUES ('" + new BigInteger(1, m.digest()).toString(16) + "' , ' " + fileName + "', '" + fileSize + "', '" + creationTime + "', '" + lastModified + "', '" + filePath + "', '" + isFolder + "');";

                DBConnManager.runQuery(sql);
                return true;
            }

        }
        return false;
    }

    /**
     * Remove file or folder from the database. This function check if file or
     * folder is already indexed in database and if it is already indexed, try
     * to remove from the database.
     * <p>
     *
     * @param filePath string containing the entire path to the file
     *
     * @return true if file was removed or false if the file/folder is not
     * indexed.
     *
     * @see DAOFiles
     */
    public synchronized static boolean removeFile(String filePath) {
        if (checkFileExistance(filePath) == true) {
            String sql = "SELECT * FROM files_n_folders "
                    + "WHERE files_n_folders.fileID = '" + filePath + "';";
            ResultSet rs = DBConnManager.runQueryAndReturn(sql);

            try {
                rs.next();
                //if just a file, remove it and it's mapping
                if (rs.getBoolean("isFolder") == false) {
                    sql = "DELETE FROM files_n_folders WHERE fileID = " + rs.getBigDecimal("fileID") + ";";
                    DBConnManager.runQueryAndReturn(sql);

                    sql = "DELETE FROM file_map WHERE fileID=" + rs.getBigDecimal("fileID") + ";";
                    DBConnManager.runQueryAndReturn(sql);
                } //if it's a folder, remove it and every files associated to its mapping
                else {

                }
            } catch (SQLException ex) {
                Logger.getLogger(DAOFiles.class.getName()).log(Level.SEVERE, null, ex);
            }

            return true;
        }
        return false;
    }

    /**
     * Insert file or folder mapping from the database. This function check if
     * file or folder is already indexed in database and if it is already
     * indexed, try to map it to the parent folder.
     * <p>
     *@param fileName string cointaining the file name
     * @param filePath string containing the entire path to the file
     *
     * @return true if file was removed or false if the file/folder is not
     * indexed.
     *
     * @see DAOFiles
     */
    public synchronized static boolean mapFile(String fileName, String filePath) {
        if (checkFileExistance(filePath) == true) {
            MessageDigest m = null;
            MessageDigest m2 = null;
            try {
                m = MessageDigest.getInstance("MD5");
                m2 = MessageDigest.getInstance("MD5");
            } catch (NoSuchAlgorithmException ex) {
                Logger.getLogger(DAOFiles.class.getName()).log(Level.SEVERE, null, ex);
            }
            if (m != null && m2 != null) {
                m.update(filePath.getBytes(), 0, filePath.length());
                String folderPath = filePath.replace(fileName, "");
                m2.update(folderPath.getBytes(), 0, folderPath.length());
                String sql = "INSERT INTO file_map (folderid, fileid)"
                        + " VALUES ('" + new BigInteger(1, m.digest()).toString(16) + "', '" + new BigInteger(1, m2.digest()).toString(16) + "');";
                ResultSet rs = DBConnManager.runQueryAndReturn(sql);

                /*
                try {
                    rs.next();
                    //if just a file, remove it and it's mapping
                    if (rs.getBoolean("isFolder") == false) {
                        sql = "DELETE FROM files_n_folders WHERE fileID = " + rs.getBigDecimal("fileID") + ";";
                        DBConnManager.runQueryAndReturn(sql);

                        sql = "DELETE FROM file_map WHERE fileID=" + rs.getBigDecimal("fileID") + ";";
                        DBConnManager.runQueryAndReturn(sql);
                    } //if it's a folder, remove it and every files associated to its mapping
                    else {

                    }
                } catch (SQLException ex) {
                    Logger.getLogger(DAOFiles.class.getName()).log(Level.SEVERE, null, ex);
                }
                */
                return true;
            }
            return false;
        }
        return false;
    }
}
