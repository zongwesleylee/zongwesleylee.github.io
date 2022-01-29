#ifndef App_h
#define App_h

#include <vector>
#include "GlutApp.h"
#include "Game.h"

class App: public GlutApp {

    Game* game;

public:
    
    App(int argc, char** argv, int width, int height, const char* title);
    
    void draw() const;
    
    void keyDown(unsigned char key, float x, float y);
    
    void run();

    ~App();
};

#endif
