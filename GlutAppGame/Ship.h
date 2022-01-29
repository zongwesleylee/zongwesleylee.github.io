#pragma one

#include "TexRect.h"

class Ship: public TexRect{

	float x;
	float y;
	float w;
	float h;

public:
	Ship(const char* filename, float x, float y, float w, float h): TexRect(filename, x, y, w, h){
		this->x = x;
		this->y = y;
		this->w = w;
		this->h = h;
	}

	float getX() const {
		return x;
	}

	float getY() const {
		return y;
	}

	float getH() const {
		return h;
	}

	float getW() const {
		return w;
	}

	void setX(float X){
		this->x = x;
	}

	void setY(float y){
		this->y = y;
	}

	//moves ship once key is pressed
	void keyDown(unsigned char key, float x, float y){
		if (key == 119 && this->y < 0.75){ //w
			this->y += y;
		}
		else if (key == 97 && this->x > -0.8){ //a
			this->x -= x;
		}
		else if (key == 115 && this->y > -0.75){ //s
			this->y -= y;
		}
		else if (key == 100 && this->x < 0.8){ //d 
			this->x += x;
		}
	}

	//makes ship move left and once it passes screen, switches to the other side
	void autoMovement(){
		if(this->x > -1.2){
			this->x -= 0.05;
			if(this->x < -1.05){
				this->x = 1.05;
			}
		}
	}

	//moves ship to another location
	void newMove(){
		this->x += 0.2;
	}

	//removes all ships
	void remove(){
		this->y = 2;
	}

	void draw(float z = 0){
		glBindTexture( GL_TEXTURE_2D, texture_id );
		glEnable(GL_TEXTURE_2D);
		
		glBegin(GL_QUADS);
		glColor4f(1, 1, 1, 1);
		glTexCoord2f(0, 0);
		glVertex3f(x, y - h, z);
		
		glTexCoord2f(0, 1);
		glVertex3f(x, y, z);
		
		glTexCoord2f(1, 1);
		glVertex3f(x+w, y, z);
		
		glTexCoord2f(1, 0);
		glVertex3f(x+w, y - h, z);
		
		glEnd();
		
		glDisable(GL_TEXTURE_2D);
	}

	~Ship(){
	}
};