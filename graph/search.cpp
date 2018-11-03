#include<bits/stdc++.h>
using namespace std;
using namespace std::chrono;

typedef vector<int> vi;

class node{
    public:
      vector<pair<int, int>> adjList;    //ind, wt
      bool explored = false;
};


class queueNode{
    public:
      int dist;
      int ind;
      queueNode(int x, int y){
          dist = x;
          ind = y;
      }
};

class myCompare{
    public:
    int operator()(const queueNode &s1, const queueNode &s2){
        return s1.dist > s2.dist;
    }
};

int main()
{
    int n, m;
    cin >> n >> m;
    cout << n << " "<< m << endl;
    vector<node> v(n);
    for (int i = 0; i < m; i++){
        int a, b, wt;
        cin >> a >> b >> wt;
        v[a].adjList.push_back(make_pair(b, wt));
    }
    
    priority_queue<queueNode, vector<queueNode>, myCompare> pq;
    pq.push(queueNode(0, 0));

    auto start = high_resolution_clock::now();
    while(!pq.empty()){
        queueNode top = pq.top();
        pq.pop();
        if (top.ind == n - 1)    //goal
        {
            cout << "Reachable\n";
            cout<<"Cost = "<<top.dist<<endl;
            break;
        }

        if(v[top.ind].explored == true){
             continue;
        }

        v[top.ind].explored = true;

        for(auto p:v[top.ind].adjList){
            int i = p.first;
            int wt = p.second;
            if(v[i].explored == false){         //expansion of s
                pq.push(queueNode(top.dist + wt, i));
            }
            
            // v[top.ind].explored = true;     //Add s to explore set
        }
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start); 
  
    cout << "Time taken by function: "
         << duration.count() << " microseconds" << endl;
   }

