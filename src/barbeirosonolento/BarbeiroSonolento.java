/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package barbeirosonolento;

/**
 *
 * @author EuristenedeSantos
 */
public class BarbeiroSonolento {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Barbeiro barbeiro1 = new Barbeiro(2, 8, "João");
        Barbeiro barbeiro2 = new Barbeiro(2, 8, "Pedro");
        Barbeiro barbeiro3 = new Barbeiro(2, 8, "Jose");
        Thread threadBarbeiro1 = new Thread(barbeiro1);
        Thread threadBarbeiro2 = new Thread(barbeiro2);
        Thread threadBarbeiro3 = new Thread(barbeiro3);
        threadBarbeiro1.start();
        threadBarbeiro2.start();
        threadBarbeiro3.start();
    }
    
}
