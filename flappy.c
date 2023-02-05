#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <time.h>
#include <unistd.h>

#define SPEED 10
#define HIGHT 30
#define WIDTH 100
int nic = 0;
int TOWER_1 = 0;
int TOWER_2 = WIDTH - 20;
int TOWER_3 = WIDTH - 40;

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

int tower_generator(WINDOW* win, int* random_1, int* random_2, int* random_3)
{
    if (TOWER_1 <= 0) {
        srand(time(0));
        *random_1 = rand() % (HIGHT - 10) + 2;
        TOWER_1 = WIDTH - 1;
    }
    for (int i = 0; i < *random_1; i++) {
        mvwaddstr(win, i, TOWER_1, "#");
        refresh();
    }
    for (int i = *random_1 + 5; i < HIGHT - 1; i++) {
        mvwaddstr(win, i, TOWER_1, "#");
        refresh();
    }
    TOWER_1--;
    if (TOWER_2 <= 0) {
        srand(time(0));
        *random_2 = rand() % (HIGHT - 10) + 2;
        TOWER_2 = WIDTH - 1;
    }
    for (int i = 0; i < *random_2; i++) {
        mvwaddstr(win, i, TOWER_2, "#");
        refresh();
    }
    for (int i = *random_2 + 5; i < HIGHT - 1; i++) {
        mvwaddstr(win, i, TOWER_2, "#");
        refresh();
    }
    TOWER_2--;
    if (TOWER_3 <= 0) {
        srand(time(0));
        *random_3 = rand() % (HIGHT - 10) + 2;
        TOWER_3 = WIDTH - 1;
    }
    for (int i = 0; i < *random_3; i++) {
        mvwaddstr(win, i, TOWER_3, "#");
        refresh();
    }
    for (int i = *random_3 + 5; i < HIGHT - 1; i++) {
        mvwaddstr(win, i, TOWER_3, "#");
        refresh();
    }
    TOWER_3--;
}

bool colision(int bird, int random_1, int random_2, int random_3)
{
    if (bird >= HIGHT - 1) {
        return true;
    }
    if (bird <= 0) {
        return true;
    }

    if (TOWER_1 == WIDTH / 3 - 9) {
        if (bird >= random_1 -1 && bird <= random_1 + 5) {
            nic++;
        } else {
            return true;
        }
    }
    if (TOWER_2 == WIDTH / 3 - 9) {
        if (bird >= random_2 -1&& bird <= random_2 + 5) {
            nic++;
        } else {
            return true;
        }
    }
    if (TOWER_3 == WIDTH / 3 - 9) {
        if (bird >= random_3 -1 && bird <= random_3 + 5) {
            nic++;
        } else {
            return true;
        }
    }

    return false;
}

int main()
{
    initscr();
    noecho();
    curs_set(FALSE);
    int random_1 = 10;
    int random_2 = 12;
    int random_3 = 15;

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
        tower_generator(win, &random_1, &random_2, &random_3);
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
                jump = 4;
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
        if (colision(bird, random_1, random_2, random_3)) {
            mvwprintw(win, 10, 10, "GAME OVER");
            wrefresh(win);
            break;
        }
    }

    char end = 's';
    while (end != '\n') {
        end = getch();
    }
    clear();

    endwin();
    return 0;
}