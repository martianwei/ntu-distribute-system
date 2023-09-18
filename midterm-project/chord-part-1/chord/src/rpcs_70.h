#ifndef RPCS_H
#define RPCS_H

#include "chord.h"
#include "rpc/client.h"
#include<vector>
#include<string>
#include <cmath>
#include <unistd.h>
Node self, successor, predecessor;
bool start = false;
const int m = 4;
std::vector<Node> fingerTable(m);
// std::vector<Node> successorList(m);
int next = 0;
// int liveSuccessorIdx = 0;
// 判斷 id 是否在 (start, end] 區間內
bool in_interval(uint64_t id, uint64_t start, uint64_t end) {
  if (start < end)
    return id > start && id <= end;
  else
    return id > start || id <= end;
}

Node closest_preceding_node(uint64_t id){
  for(int i = m - 1; i >= 0; i--){
    if(in_interval(fingerTable[i].id , self.id , id)){
      std::cout << "closest_preceding_node: " << fingerTable[i].id << std::endl;
      return fingerTable[i];
    }
  }
  std::cout << "closest_preceding_node: " << successor.id << std::endl;
  return successor;
}

Node get_info() { return self; } // Do not modify this line.

void create() {
  start = true;
  predecessor = self;
  successor = self;
  for(auto i = 0; i < m; i++)
    fingerTable[i] = self;
  //註解
  std::cout << "create() " \
            << "self.id: " << self.id << " successor.id: " << successor.id \
            << " fingerTable[0].id: " << fingerTable[0].id \
            << std::endl;
}

void join(Node n) {
  start = true;
  predecessor.ip = "";
  rpc::client client(n.ip, n.port);
  successor = client.call("find_successor", self.id).as<Node>();
  for(auto i = 0; i < m; i++)
    fingerTable[i] = successor;
  rpc::client client2(successor.ip, successor.port);
  client2.call("notify" , self);
  //註解
  std::cout << "join() " \
              << "self.id: " << self.id << " successor.id: " << successor.id \
              << std::endl;
}


Node find_successor(uint64_t id) {
  // TODO: implement your `find_successor` RPC
  //註解
  std::cout << "find_successor() " \
              << "self.id: " << self.id << " successor.id: " << successor.id << " find_id: " << id \
              << std::endl;
  if(in_interval(id , self.id , successor.id)){
    std::cout << "find: " << successor.id << std::endl;
    return successor;
  }
  else{
    Node next = closest_preceding_node(id);
    
    rpc::client client(next.ip, next.port);
    return client.call("find_successor", id).as<Node>();
    
  }
}

void stabilize(){
  if(start){
    try{
      //註解
      std::cout << "stabilize() " \
                << "self.id: " << self.id << " successor.id: " << successor.id \
                << std::endl;
      rpc::client client(successor.ip, successor.port);
      Node newSuccessor = client.call("get_predecessor").as<Node>();
      if(successor.id == newSuccessor.id){
        //do nothing
      }
      else if(in_interval(newSuccessor.id , self.id , successor.id)){
        //註解
        std::cout << "stabilize() found newSuccessor " \
                  << "self.id: " << self.id << " newSuccessor.id: " << newSuccessor.id \
                  << std::endl;
        successor = newSuccessor;
      }
      rpc::client client2(successor.ip, successor.port);
      client2.call("notify" , self);
    }catch (std::exception &e) {
      //註解
      // std::cout << "pid[" << ::getpid() << "]" \
      //           <<"successor " <<" dead"<< std::endl;
    }
  }
}

void notify(Node n){
  if(n.id == predecessor.id){
    //do nothing
  }
  else if(predecessor.ip == "" || in_interval(n.id , predecessor.id , self.id)){
    //註解
    std::cout << "notify() change predecessor " \
              << "self.id: " << self.id << " new predecessor: " << n.id\
              << std::endl;
    predecessor = n;
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
      std::cout << "fix_fingerTable() " \
                << "self.id: " << self.id << " fingerTable["<< next <<"]: " << fingerTable[next].id \
                << std::endl;
      next = next + 1;
      if(next >= m)
        next = 0;
    }catch (std::exception &e) {
      std::cout << "fix_fingerTable() fail" << std::endl; 
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
}

void register_periodics() {
  add_periodic(check_predecessor);
  add_periodic(stabilize);
  add_periodic(fix_fingerTable);
}

#endif /* RPCS_H */
