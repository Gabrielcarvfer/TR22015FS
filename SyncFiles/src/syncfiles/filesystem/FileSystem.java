/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.filesystem;

import java.io.File;
import java.util.ArrayList;
import java.util.Collection;
import syncfiles.dao.DAOFiles;
import syncfiles.dao.DBConnManager;

/**
 *
 * @author Gabriel
 */
public class FileSystem {
    
    /**
    * Index folders and files to the database. 
    * The file argument must specify the base folder {@link File}, that is going
    * to be used to index all subfolders and their files to the database.
    * <p>
    *
    * @param  folder the base folder to index
    * @return boolean
    * @see    FileSystem
    */
    public boolean reIndexFolder(File folder)
    {
        Collection<File> all = new ArrayList<>();
        addTree(folder, all);
 
        for (File temp : all) 
        {
            FileFolderIndexThread indexer = new FileFolderIndexThread(temp);
            indexer.start();
            
        }
        for (File temp : all)
        {
            FolderRepairThread repairer = new FolderRepairThread(temp);
            repairer.run();
        }
  
        DBConnManager.closeDatabaseConnection();
        return true;
    }

    /**
    * Discover every subfolder and subfile from a base folder. 
    * This recursive function discover every folder and file
    * inside of the folder passed through the file parameter {@link File} 
    * and add them to the collection of files parameter {@link Collection<File>}.
    * <p>
    *
    * @param  file the base folder to index
    * @param  all a collection of folders and files
    * @see    FileSystem
    */
    private void addTree(File file, Collection<File> all)
    {
        File[] children = file.listFiles();
        if (children != null) 
        {
            for (File child : children) 
            {
                all.add(child);
                addTree(child, all);
            }
        }
    }
    
    /**
    * Remove file of folder indicated. 
    * This function deletes a file or folder that is indicated
    * in path parameter {@link String}.
    * <p>
    *
    * @param  path string cointaining the directory of file that should be removed
    * @return boolean
    * @see    FileSystem
    */
    public boolean removeFileFolder(String path)
    {
        File file = new File(path);
        DAOFiles.removeFile(path);
        return file.delete();
    }
}


