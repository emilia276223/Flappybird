#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <time.h>
#include <unistd.h>

#define SPEED 10
#define HIGHT 30
#define WIDTH 100

int kbhit(void)
{
    struct timeval tv;
    fd_set read_fd;

    tv.tv_sec = 0;
    tv.tv_usec = 0;
    FD_ZERO(&read_fd);
    FD_SET(0, &read_fd);

    if (select(1, &read_fd, NULL, NULL, &tv) == -1)
        return 0;

    if (FD_ISSET(0, &read_fd))
        return 1;

    return 0;
}

bool colision(int bird)
{
    if (bird >= HIGHT - 1) {
        return true;
    }
    if (bird <= 0) {
        return true;
    }
    return false;
}

int main()
{
    initscr();
    noecho();
    curs_set(FALSE);

    WINDOW* win = newwin(HIGHT, WIDTH, 1, 1);
    keypad(win, TRUE);
    refresh();
    box(win, 0, 0);
    wrefresh(win);

    int bird = HIGHT / 2;
    int action = 's';
    int jump = 0;

    wrefresh(win);

    while (1) {
        werase(win);
        mvwaddstr(win, bird, WIDTH / 3 - 9, "O");
        box(win, 0, 0);
        wrefresh(win);

        if (jump > 0) {
            jump--;
        }

        if (kbhit()) {
            if (jump == 0) {
                action = wgetch(win);
            }
            if (action == ' ') {
                jump = 5;
            }
        }
        if (jump > 0) {
            bird--;
        }
        if (jump <= 0) {
            bird++;
            wrefresh(win);
        }
        action = 's';
        usleep(1000000 / SPEED);
        if(colision(bird)) {
            mvwprintw(win, 10, 10, "GAME OVER");
            wrefresh(win);
            //endwin();
            break;
        }
    }
    
    char end = 's';
    while(end != '\n') {
        end = getch();
    }
    clear();

    endwin();
    return 0;
}