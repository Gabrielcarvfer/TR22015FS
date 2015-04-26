/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gabriel
 */
public class DBConnectionManager {
    
    private static Connection c;
    
    public static boolean createConnection ()
    {
        try {
            Class.forName("org.hsqldb.jdbcDriver").newInstance();
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException e) {
            System.out.println("ERROR: failed to load HSQLDB JDBC driver.");
            return false;
        }
        try {
            DBConnectionManager.c = DriverManager.getConnection("jdbc:hsqldb:hsql:file:syncdb", "sa", "");
        } catch (SQLException ex) {
            Logger.getLogger(DBConnectionManager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
        return true;
    }
     
    public static Connection getConnection()
    {
        return DBConnectionManager.c;
    }
}
