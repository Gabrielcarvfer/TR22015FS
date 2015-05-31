/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.dao;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import syncfiles.filesystem.FileFolderIndexThread;

/**
 *
 * @author Gabriel
 */
public class DAOFiles {

    /**
    * Check if file or folder already exists in database. 
    * This function check if file or folder is already indexed in database
    * returning true or false.
    * <p>
    * 
    * @param filePath string containing the path to a file or folder
    * @return true if file does exist or false if it does not
    * @see    DAOFiles
    */
    private synchronized static boolean checkFileExistance(String filePath)
    {
        DBConnManager.initializeDatabaseConnection();
        //Cria select, futuramente em DAOFiles
        String sql = "SELECT * FROM files_n_folders "
                +"WHERE files_n_folders.filepath = '" + filePath +"';";
        
        //Roda query
        ResultSet rs = DBConnManager.runQueryAndReturn(sql);
        if(rs != null)  
        {
            //Query retornou com sucesso
            try 
            {
                //Checa se arquivo existe
                if(rs.next() == true)
                {
                    //File exists
                    return true;
                }
            } 
            catch (SQLException ex) 
            {
                Logger.getLogger(FileFolderIndexThread.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        return false;
    }
    
    
    /**
    * Insert new file or folder to the database. 
    * This function check if file or folder is already indexed in database
    * and if it is not indexed yet, try to insert it to the database.
    * <p>
    * 
    * @param fileName string containing the file or folder name
    * @param fileSize file size in bytes
    * @param creationTime timestamp of file creation
    * @param lastModified timestamp of last file modification
    * @param filePath string containing the entire path to the file
    * @param isFolder boolean value indicating that the file is really a file, or a folder
    * 
    * @return true if file was inserted or already exists, or 
    *  not if any of those failed
    * 
    * @see    DAOFiles
    */
    public synchronized static boolean insertNewFile
        (String fileName, long fileSize, String creationTime, String lastModified, String filePath, boolean isFolder)
    {
        if(checkFileExistance(filePath) != true)
        {
            String sql = "INSERT INTO files_n_folders (filename, filesize, creationtime, lastmodified, filepath, isfolder)"
                        +" VALUES ('" + fileName + "', '" + fileSize + "', '" + creationTime + "', '" + lastModified +"', '" + filePath + "', '" + isFolder +"');";

            DBConnManager.runQuery(sql);
            return true;
        }
        return false;
    }
        
        
        /**
    * Remove file or folder from the database. 
    * This function check if file or folder is already indexed in database
    * and if it is already indexed, try to remove from the database.
    * <p>
    * 
    * @param filePath string containing the entire path to the file
    * 
    * @return true if file was removed or false
    * if the file/folder  is not indexed.
    * 
    * @see    DAOFiles
    */
    public synchronized static boolean removeFile(String filePath)
    {
        if(checkFileExistance(filePath) == true)
        {
       
            String sql = "DELETE FROM files_n_folders WHERE filePath = '" + filePath + "';";
            DBConnManager.runQuery(sql);
            return true;
        }
        return false;
    }
}
