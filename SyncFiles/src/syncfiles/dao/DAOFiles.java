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
