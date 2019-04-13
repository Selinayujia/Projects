//
//  main.cpp
//  rec03
//
//  Created by Selina on 09/02/2018.
//  Copyright © 2018 Selina. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <ctime>
using namespace std;

int produce_rand();
bool isVisible(int row, int col);


class Minesweeper
{
private:
    vector <vector<int>> number_repre;
    vector <vector<bool>> if_visable;
    
public:
    
    Minesweeper()
    {
        srand((unsigned)time(0));
        for(size_t row=0;row<10;++row)
        {
            vector<int> number_repre_col(10);
            number_repre.push_back(number_repre_col);
        }
        for(size_t row=0; row<number_repre.size();++row)
        {
            for(size_t col=0; col<number_repre[row].size();++col)
            {
                int rand=produce_rand();
                if (rand<10)
                {
                    number_repre[row][col]=-1;
                }
                else
                {
                    number_repre[row][col]=0;
                }
            }
        }
        for(size_t row=0;row<10;++row)
        {
            vector<bool> if_visable_col(10);
            if_visable.push_back(if_visable_col);
        }
        for(size_t row=0; row<if_visable.size();++row)
        {
            for(size_t col=0; col<if_visable[row].size();++col)
            {
                if_visable[row][col]=false;
            }
        }
    }
    
    void display(bool done)
    {
        if(done== true)
        {
            
            for(size_t row=0; row<number_repre.size();++row)
            {
                for(size_t col=0; col<number_repre[row].size();++col)
                {
                    if(number_repre[row][col]==-1)
                    {
                        cout<<'b'<<' ';
                    }
                    else
                    {
                        cout<<'-'<<' ';
                    }
                    
                }
                cout<<endl;
            }
        }
        else
        {
            for(size_t row=0; row<number_repre.size();++row)
            {
                for(size_t col=0; col<number_repre[row].size();++col)
                {
                    if(if_visable[row][col]==true)
                    {
                        cout<<number_repre[row][col]<<' ';
                    }
                    else
                    {
                        cout<<'-'<<' ';
                    }
                }
                
                cout<<endl;
            }
        }
        
        
    }
    
    
    bool done()
    {
        for(int row=0; row<number_repre.size();++row)
        {
            for(int col=0; col<number_repre[row].size();++col)
            {
                if(number_repre[row][col]!=-1 && isVisible(row,col))
                {
                    continue;;
                }
                else
                {
                    return false;
                }
            }
        }
        return true;
    }
    
    
    
    
    
    bool play(int row, int col)
    {
        if (number_repre[row][col]==-1)
        {
            return false;
        }
        else
        {
            int count=0;
            vector<vector<int>> to_do_list;
            for (int r=row-1;r<=row+1;++r)
            {
                for (int c=col-1;c<=col+1;++c)
                {
                    if((validCol(c))&&(validRow(r))&&(!isVisible(r, c)))
                    {
                        if(number_repre[r][c]==-1)
                        {
                            count+=1;
                        }
                        else
                        {
                            if((r==row && c==col))
                            {
                                continue;
                            }
                            else
                            {
                                vector<int> r_c;
                                r_c.push_back(r);
                                r_c.push_back(c);
                                
                                to_do_list.push_back(r_c);
                            }
                        }
                    }
                }
            }
            if(count!=0)
            {
                number_repre[row][col]=count;
                if_visable[row][col]=true;
                return true;
            }
            else //no bombs beside
            {
                if_visable[row][col]=true;
                
                for (size_t i=0;i<to_do_list.size();++i)
                {
                    play(to_do_list[i][0],to_do_list[i][1]);
                }
                return true;
                
            }
            
        }
        
    }
    
    
    
    bool isVisible(int row, int col)
    {
        if(if_visable[row][col]==true)
        {
            return true;
        }
        return false;
    }
    
    
    bool validRow( int row)
    {
        if( (row>=0) && (row<10))
        {
            return true;
        }
        return false;
    }
    
    bool validCol(int col)
    {
        if( (col>=0) && (col<10))
        {
            return true;
        }
        return false;
    }
    
    
    int produce_rand()
    {
        int random_int;
        random_int = (rand()%100);
        return random_int;
        
    }
    
    
    
};




int main()
{
    Minesweeper sweeper;
    // Continue until only invisible cells are bombs
    while (!sweeper.done()) {
        sweeper.display(false); // display board without bombs
        
        int row_sel = -1, col_sel = -1;
        while (row_sel == -1) {
            // Get a valid move
            int r, c;
            cout << "row? ";
            cin >> r;
            if (!sweeper.validRow(r)) {
                cout << "Row out of bounds\n";
                continue;
            }
            cout << "col? ";
            cin >> c;
            if (!sweeper.validCol(c)) {
                cout << "Column out of bounds\n";
                continue;
            }
            if (sweeper.isVisible(r,c)) {
                cout << "Square already visible\n";
                continue;
            }
            row_sel = r;
            col_sel = c;
        }
        // Set selected square to be visible. May effect other cells.
        if (!sweeper.play(row_sel,col_sel)) {
            cout << "Sorry, you died..\n";
            sweeper.display(true); // Final board with bombs shown
            exit(0);
        }
    }
    // Ah! All invisible cells are bombs, so you won!
    cout << "You won!!!!\n";
    sweeper.display(true); // Final board with bombs shown
    
}



