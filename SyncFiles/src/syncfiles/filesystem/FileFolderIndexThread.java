/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.filesystem;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import syncfiles.dao.DBConnManager;

/**
 *
 * @author Gabriel
 */
public class FileFolderIndexThread extends Thread
{
    private Path path;
    public FileFolderIndexThread (File file){
        this.path = file.toPath();
    }
    @Override
    public void run()
    {
        
        System.out.println("FileIndexThread running\n");
        BasicFileAttributes attr = null;
        
        try {
            attr = Files.readAttributes(this.path, BasicFileAttributes.class);
            System.out.println("fileName: " + path.getFileName());
            System.out.println("creationTime: " + attr.creationTime());
            System.out.println("lastAccessTime: " + attr.lastAccessTime());
            System.out.println("lastModifiedTime: " + attr.lastModifiedTime());
            System.out.println("isDirectory: " + attr.isDirectory());
            System.out.println("isOther: " + attr.isOther());
            System.out.println("isRegularFile: " + attr.isRegularFile());
            System.out.println("isSymbolicLink: " + attr.isSymbolicLink());
            System.out.println("size: " + attr.size());
            
        } catch (IOException ex) {
            Logger.getLogger(FileFolderIndexThread.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        /*Futuramente em DAOFiles*/
                
        //Cria select, futuramente em DAOFiles
        String sql = "SELECT * FROM files_n_folders"
                + "WHERE files_n_folders.filepath = '" + path.getFileName() +"';";
        
        //Roda query
        ResultSet rs = DBConnManager.runQuery(sql);
        if(rs != null)  
        {
            try {
                //Checa se arquivo existe
                int fileId = rs.getInt("files.fileid");
                int isFolder = rs.getInt("files.isfolder");
                System.out.print("File Id: " + fileId);
                System.out.print(", Is Folder?: " + isFolder);
            } catch (SQLException ex) {
                Logger.getLogger(FileFolderIndexThread.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        else
        {
            sql = "INSERT INTO files_n_folders "
                    + "VALUES ('" + path.getFileName() + "', '" + attr.size() + "', '" + attr.creationTime() + "', '" + attr.lastModifiedTime() +"', '" + path.getFileName() + "', '" + attr.isDirectory() +"');";

            rs = DBConnManager.runQuery(sql);
       
        }
    }
}
