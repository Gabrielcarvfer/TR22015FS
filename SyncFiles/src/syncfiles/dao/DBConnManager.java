/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gabriel
 */
public class DBConnManager 
{
    private static final String DB_URL = "jdbc:sqlite:sync.db";
    private static Connection conn;
    private static Statement stmt;
    private static boolean driverInitialized;
    
    public static boolean initializeDatabaseConnection()
    {
        try 
        {
            if(driverInitialized == false)
            {
                Class.forName("org.sqlite.JDBC");
                driverInitialized = true;
                conn = DriverManager.getConnection(DB_URL);
                stmt = conn.createStatement();
            }
        } catch (ClassNotFoundException | SQLException ex) {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
         return true;
    }
    
    public static boolean initializeDatabaseConnection(String serverAddress)
    {
        try 
        {
            if(driverInitialized == false)
            {
                Class.forName("org.sqlite.JDBC");
                driverInitialized = true;
                conn = DriverManager.getConnection(serverAddress);
                stmt = conn.createStatement();
            }
        } catch (ClassNotFoundException | SQLException ex) {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
        return true;
    }
    
    public static ResultSet runQuery(String sql)
    {
        try {
            ResultSet rs = stmt.executeQuery(sql);
            return rs;
        } catch (SQLException ex) {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }
    
    public static boolean closeDatabaseConnection(){   
        try {
            stmt.close();
            conn.close();
            return true;
        } catch (SQLException ex) {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
    }
  
}
