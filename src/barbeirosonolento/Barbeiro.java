/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package barbeirosonolento;

import java.util.Random;

/**
 *
 * @author EuristenedeSantos
 */
public class Barbeiro implements Runnable{

    private int cadeiraEspera;// Para definir quantas pessoas irá esperar
    boolean cadeiraBOculpada = false, barbeiroDormindo = false;//Estado da Cadeira e do Barbeiro
    int clientes[];// Vetor com o número aleatório de clientes
    private String nome;//Nome da tread criada
    private int clientesNovos;
    int numClientes = 0;

    public Barbeiro(int cadeiraEspera, int clientes, String nome) {
        clientesNovos = clientes;
        this.nome = nome;
        this.cadeiraEspera = cadeiraEspera;
        System.out.println("O barbeiro "+nome+" acabou de chegar no salão.");
    }
    
    public void Clientes(){
        Random rand = new Random();
        numClientes = rand.nextInt(clientesNovos);
        clientes = new int[numClientes];
        
        for(int i = 0; numClientes < clientes.length; i++){
            clientes[i] = i;
        }
    }
    
    public void Dormir() throws InterruptedException{
        System.out.println("Não existe cliente na barbearia do barbeiro "+nome+".");
        System.out.println("O barbeiro "+nome+" está esperando clientes!");
        System.out.println("O barbeiro "+nome+" Dormiu......................");
        Thread.sleep(2000);
        System.out.println("A cadeira do barbeiro "+nome+" está livre");
        Clientes();
    }

    
   public void CortarCabelo() throws InterruptedException{
       if(numClientes != 0){
           if(numClientes > 1 && cadeiraBOculpada == false){
               System.out.println("Entrou "+numClientes+" na barbearia");
           }else{
               System.out.println("Existe "+numClientes+" esperando atendimento");
           }
           System.out.println("Um cliente ocupou a cadeira do barbeiro");
           numClientes--;
           System.out.println("O barbeiro "+nome+" está cortando o cabelo de um cliente");
           cadeiraBOculpada = true;
           Thread.sleep(1000);
           if(numClientes > cadeiraEspera){
               int cli = numClientes - cadeiraEspera;
               numClientes = numClientes - cli;
               
               for(int i = 0; i < clientes.length - 1; i++){
                   clientes[i] = 0;
               }
               for(int j = 0; j < numClientes; j++){
                   clientes[j] = j + 1;
               }
               System.out.println(cli+" clientes foram embora");
               System.out.println(numClientes+" estão esperando atendimento");
           }
           System.out.println("Um cliente foi atendido pelo barbeiro "+nome);
       }else if(numClientes == 1){
           System.out.println("A cadeira do barbeiro "+nome+" está livre!");
           System.out.println("A cadeira do barbeiro "+nome+" está ocupada e não existe cliente esperando");
           Thread.sleep(1000);
           numClientes--;
           System.out.println("Um cliente foi atendido pelo barbeiro "+nome);
       }else{
           System.out.println("A cadeira do barbeiro "+nome+" está livre");
           cadeiraBOculpada = false;
       }
   }
   
    @Override
    public void run() {
        while(true){
            if(numClientes <= 0){
                try{
                    Dormir();
                }catch(InterruptedException ex){
                    System.out.println(ex);
                }
            }else{
                try{
                    CortarCabelo();
                }catch(InterruptedException ex){
                    System.out.println(ex);
                }
            }
        }
    }   
}
