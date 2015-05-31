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
import java.util.logging.Level;
import java.util.logging.Logger;
import syncfiles.dao.DAOFiles;

/**
 *
 * @author gabriel
 */
public class FileMapThread {
            private Path path;
            private static final String userDir = System.getProperty("user.dir");

            /**
            * Return a instance of File Map indexer. 
            * The file argument must specify a file or folder {@link File}, that is going
            * to be mapped to the parent folder.
            * <p>
            *
            * @param  file a file or folder to index
            * @see         FileFolderIndexThread
            */
            public FileMapThread (File file){
                         this.path = file.toPath();

            }
            public synchronized void run()
            {

                        //System.out.println("FileIndexThread running\n");
                        BasicFileAttributes attr = null;

                        try {
                            attr = Files.readAttributes(this.path, BasicFileAttributes.class);
                        } catch (IOException ex) {
                            Logger.getLogger(FileIndexThread.class.getName()).log(Level.SEVERE, null, ex);
                        }

                        if (attr != null)
                        {
                            DAOFiles.insertNewFile (path.getFileName().toString(), attr.size(), attr.creationTime().toString(),
                                    attr.lastModifiedTime().toString(), path.toString().replace(userDir, ""), attr.isDirectory() );  
                        }
            }
}
