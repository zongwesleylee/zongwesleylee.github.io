#ifndef Game_h
#define Game_h

#include "Ship.h"
#include <deque>
#include <vector>
#include "GlutApp.h"
#include "TexRect.h"

class Game{
    Ship* ship;
    std::deque<Ship*> enemys;
    TexRect* bg;

    unsigned int score = 0;
    unsigned int interval;
    bool gameover = false;

public:
    Game();

    void draw();
    void keyDown(unsigned char key);
    void keyUp(unsigned char key);
    friend void timer(int id);

    ~Game();
};

#endif