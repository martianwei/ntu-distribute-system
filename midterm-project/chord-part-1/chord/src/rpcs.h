#ifndef RPCS_H
#define RPCS_H

#include "chord.h"
#include "rpc/client.h"
#include<vector>
#include<string>
#include <cmath>
#include <unistd.h>
Node self, successor, predecessor;

//do not run periodic func before create or join. 
bool start = false;

//finger table size
const int m = 4;

//successorList size
const int r = 3;

std::vector<Node> fingerTable(m);
std::vector<Node> successorList(r);

// next fix_fingerTable fix index 
int next = 0;

// nearest alive successor index
int aliveSuccessorIdx = 0;

// check whether id in (start, end] interval
bool in_interval(uint64_t id, uint64_t start, uint64_t end) {
  if (start < end)
    return id > start && id <= end;
  else
    return id > start || id <= end;
}

// find closest preceding node
Node closest_preceding_node(uint64_t id){
  for(int i = m - 1; i >= 0; i--){
    if(in_interval(fingerTable[i].id , self.id , id)){
      // std::cout << "closest_preceding_node: " << fingerTable[i].id << std::endl;
      return fingerTable[i];
    }
  }
  // std::cout << "closest_preceding_node: " << successor.id << std::endl;
  return successor;
}


//get info of the node
Node get_info() { return self; } // Do not modify this line.


//create node
void create() {
  predecessor = self;
  successor = self;
  for(auto i = 0; i < m; i++)
    fingerTable[i] = self;
  for(auto i = 0; i < r; i++)
    successorList[i] = self;
  //註解
  // std::cout << "create() " \
  //           << "self.id: " << self.id << " successor.id: " << successor.id \
  //           << std::endl;
  start = true;
}

// join node by n
void join(Node n) {
  predecessor.ip = "";
  rpc::client client(n.ip, n.port);
  successor = client.call("find_successor", self.id).as<Node>();
  for(auto i = 0; i < m; i++)
    fingerTable[i] = successor;
  rpc::client successorClient(successor.ip, successor.port);
  successorList = successorClient.call("get_successorList").as<std::vector<Node>>();
  successorList.insert(successorList.begin() , successor);
  successorList.pop_back();

  successorClient.call("notify" , self);
  //註解
  // std::cout << "join() " \
  //             << "self.id: " << self.id << " successor.id: " << successor.id \
  //             << std::endl;
  start = true;
}

// get successor list
std::vector<Node> get_successorList(){
  return successorList;
}

//
Node find_successor(uint64_t id) {
  // TODO: implement your `find_successor` RPC
  //註解
  // std::cout << "find_successor() " \
  //             << "self.id: " << self.id << " successor.id: " << successor.id << " find_id: " << id \
  //             << std::endl;
  if(in_interval(id , self.id , successor.id)){
    // std::cout << "found: " << successor.id << std::endl;
    return successor;
  }
  else{
    Node next = closest_preceding_node(id);
    rpc::client client(next.ip, next.port);
    try{
      Node ans = client.call("find_successor", id).as<Node>();
      return ans;
    }catch(std::exception &e){
      // std::cout << "find_successor() " \
      //           << "self.id: " <<  self.id \
      //           <<" next: " << next.id \
      //           << " fail !"<< std::endl;
      if(next.id == successor.id){
        sleep(2);
        return find_successor(id);
      }
      else{
        rpc::client client(successor.ip, successor.port);
        Node ans = client.call("find_successor", id).as<Node>();
        return ans;
      }
    }
  }
}

  

void stabilize(){
  if(start){
    while(true){
      // std::cout << "stabilize() " \
      //         << "self.id: " << self.id << " successor.id: " << successor.id \
      //         << std::endl;
      try{
        if(aliveSuccessorIdx == 0){
          rpc::client oldSuccessorClient(successor.ip, successor.port);
          Node newSuccessor = oldSuccessorClient.call("get_predecessor").as<Node>();
          if((successor.id != newSuccessor.id) & in_interval(newSuccessor.id , self.id , successor.id)){
            //註解
            // std::cout << "stabilize() found newSuccessor " \
            //           << "self.id: " << self.id << " newSuccessor.id: " << newSuccessor.id \
            //           << std::endl;
            successor = newSuccessor;
          }
        }
        rpc::client newSuccessorClient(successor.ip, successor.port);
        successorList = newSuccessorClient.call("get_successorList").as<std::vector<Node>>();
        successorList.insert(successorList.begin() , successor);
        successorList.pop_back();
        aliveSuccessorIdx = 0;
        // std::cout << "stabilize() " \
        //           << "self.id: " << self.id \
        //           << " successorList[0]:" << successorList[0].id \
        //           << " successorList[1]:" << successorList[1].id \
        //           << " successorList[2]:" << successorList[2].id \
        //           << std::endl;
        newSuccessorClient.call("notify" , self);
        return;
      }catch(std::exception &e){
        // std::cout << "stabilize() " \
        //           << "self.id: " <<  self.id \
        //           <<" successor: " << successor.id \
        //           << " fail !"<< std::endl;
        successor = successorList[++aliveSuccessorIdx];
      }
    }
  }
}

void notify(Node n){
  if(n.id != predecessor.id){ 
    if(predecessor.ip == "" || in_interval(n.id , predecessor.id , self.id)){
      //註解
      // std::cout << "notify() change predecessor " \
      //           << "self.id: " << self.id << " new predecessor: " << n.id\
      //           << std::endl;
      predecessor = n;
    }
    else{
      //check predecessor alive or not
      try{
        rpc::client predecessorClient(predecessor.ip, predecessor.port);
        Node n = predecessorClient.call("get_info").as<Node>();
      }catch(std::exception &e){
        // std::cout << "notify() change predecessor " \
        //         << "self.id: " << self.id << " new predecessor: " << n.id\
        //         << std::endl;
        predecessor = n;
      }
    }
  }
}

Node get_predecessor(){
  return predecessor;
}

void fix_fingerTable(){
  if(start){
    try{
      rpc::client client(self.ip, self.port);
      uint64_t find = (self.id + static_cast<uint64_t>(pow(2,28+next))) % static_cast<uint64_t>(pow(2,32));
      fingerTable[next] = client.call("find_successor" , find).as<Node>();
      //註解
      // std::cout << "fix_fingerTable() " \
      //           << "self.id: " << self.id << " fingerTable["<< next <<"]: " << fingerTable[next].id \
      //           << std::endl;
      next = next + 1;
      if(next >= m)
        next = 0;
    }catch (std::exception &e) {
      // std::cout << "fix_fingerTable() fail" << std::endl; 
    }
  }
}

void check_predecessor() {
  try {
    rpc::client client(predecessor.ip, predecessor.port);
    Node n = client.call("get_info").as<Node>();
  } catch (std::exception &e) {
    predecessor.ip = "";
  }
}

void register_rpcs() {
  add_rpc("get_info", &get_info); // Do not modify this line.
  add_rpc("create", &create);
  add_rpc("join", &join);
  add_rpc("find_successor", &find_successor);
  add_rpc("get_predecessor" , &get_predecessor);
  add_rpc("notify" , &notify);
  add_rpc("get_successorList", &get_successorList);
}

void register_periodics() {
  add_periodic(check_predecessor);
  add_periodic(stabilize);
  add_periodic(fix_fingerTable);
}

#endif /* RPCS_H */
