#include "Game.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include "Rect.h"
#include <string>
using namespace std;

static Game* singleton;

int width = 600, height = 600;

//allows text to be added
void renderText(
	string text,
	float x,
	float y,
	void* font = GLUT_BITMAP_HELVETICA_18,
	float r = 1,
	float g = 1,
	float b = 1
){
	glColor3f(r, g, b);
	float offset = 0;
	for (int i = 0; i < text.length(); i++) {
		glRasterPos2f(x+offset, y);
		glutBitmapCharacter(font, text[i]);
		int w = glutBitmapWidth(font, text[i]);
		offset += ((float)w / width)*2;
		}
	}


void timer(int id){
    if(singleton->gameover == false){
        //makes enemy move left and right continuously
        for(int i = 0; i <= singleton->enemys.size(); i++){
            singleton->enemys[i]->autoMovement();
        }
        
        //collision detection
        for(int i = 0; i < singleton->enemys.size(); i++){
            singleton->score = singleton->score + 1;

            //makes ship disappear when hit by enemy
            if(singleton->ship->getX() < singleton->enemys[i]->getX() + singleton->enemys[i]->getW() &&
            singleton->ship->getX() + singleton->ship->getW() > singleton->enemys[i]->getX() &&
            singleton->ship->getY() < singleton->enemys[i]->getY() + singleton->enemys[i]->getH() &&
            singleton->ship->getY() + singleton->ship->getH() > singleton->enemys[i]->getY()){
                singleton->ship->remove();
                singleton->gameover = true;
                for(int j = 0; j < singleton->enemys.size(); j++)
                    singleton->enemys[j]->remove();
            }

            //prevents enemies from overlapping
            for(int j = 0; j < singleton->enemys.size(); j++)
                if(i !=j &&
                singleton->enemys[i]->getX() < singleton->enemys[j]->getX() + singleton->enemys[j]->getW() &&
                singleton->enemys[i]->getX() + singleton->enemys[i]->getW() > singleton->enemys[j]->getX() &&
                singleton->enemys[i]->getY() < singleton->enemys[j]->getY() + singleton->enemys[j]->getH() &&
                singleton->enemys[i]->getY() + singleton->enemys[i]->getH() > singleton->enemys[j]->getY()){
                    singleton->enemys[i]->newMove();
                }
        }
        glutPostRedisplay();
        glutTimerFunc(singleton->interval, timer, id);
    }
}

Game::Game(){
    //player ship
    ship = new Ship("images/spaceship.png", -0.7, 0, 0.16, 0.12);
    
    //makes multiple enemies
    srand( (unsigned)time( NULL ) );
    for(int i = 0; i <= 50; i++){
        float randNumy = ((float) rand()/(RAND_MAX/2)) - 0.9; //random y axis
        float randNumx = ((float) rand()/(RAND_MAX/50)) + 1; //random x axis
        enemys.push_front(new Ship("images/enemy.png", randNumx, randNumy, 0.16, 0.12));
    }

    //background
    bg = new TexRect("images/Space01.png", -1, 1, 2, 2);
    
    interval = 125;
    singleton = this;
    timer(1);
}

void Game::draw(){
    bg->draw(); //draws background
	renderText("Score: ", -0.75, 0.85, GLUT_BITMAP_TIMES_ROMAN_24, 1, 1, 1);
    ship->draw(0.5); //draws player
    
    for(int i = 0; i <= enemys.size(); i++){ //draws enemies
        enemys[i]->draw(0.5);
    }

    //if game is over show text
    if(gameover == true){
        renderText("Game Over", -0.2, 0, GLUT_BITMAP_TIMES_ROMAN_24, 1, 1, 1);
        renderText(to_string(score), -0.5, 0.85, GLUT_BITMAP_TIMES_ROMAN_24, 1, 1, 1);

    }
}

void Game::keyDown(unsigned char key){
    ship->keyDown(key, 0.02, 0.02); //moves player when key is pressed
}

Game::~Game(){
    delete ship;
    delete bg;
    enemys.clear();
}