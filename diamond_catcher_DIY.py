from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

d_tx = random.randint(20,480)

d_lx, d_ly, d_rx, d_ry, d_ty, d_bx, d_by = d_tx-10, 600, d_tx+10, 600, 617, d_tx, 583
c_ltx, c_lty, c_lbx, c_lby, c_rtx, c_rty, c_rbx, c_rby = 195,20,210,2,345,20,330,2
dcr = 0.0
sp = 0.125
points = 0
r, g, b = random.uniform(0.5,1.0), random.uniform(0.5,1.0), random.uniform(0.5,1.0)
rc, gc, bc = 1.0, 1.0, 1.0
pause = False
pc = 1

def to_zone_zero(x0,y0,x1,y1):
    dx = x1 - x0
    dy = y1 - y0
    
    if dx > 0 and dy > 0:
        #zone 0/1
        if abs(dx) >= abs(dy):
            #zone 0
            return (x0,y0,x1,y1,0)
        else:
            #zone 1
            return (y0,x0,y1,x1,1)
        
    elif dx < 0  and dy > 0:
        #zone 2/3
        if abs(dx) >= abs(dy):
            #zone 3
            return (-x0,y0,-x1,y1,3)
        else:
            #zone 2
            return (y0,-x0,y1,-x1,2)
        
    elif dx < 0  and dy < 0:
        #zone 4/5
        if abs(dx) >= abs(dy):
            #zone 4
            return (-x0,-y0,-x1,-y1,4)
        else:
            #zone 5
            return (-y0,-x0,-y1,-x1,5)
    
    elif dx > 0 and dy < 0:
        #zone 6/7
        if abs(dx) >= abs(dy):
            #zone 7
            return (x0,-y0,x1,-y1,7)
        else:
            #zone 6
            return (-y0,x0,-y1,x1,6)

def to_zone_prev(li, zn):
    li1 = []

    if zn == 0:
        return li
    elif zn == 1:
        for p in li:
            li1.append((p[1],p[0]))
    elif zn == 2:
        for p in li:
            li1.append((-p[1],p[0]))
    elif zn == 3:
        for p in li:
            li1.append((-p[0],p[1]))
    elif zn == 4:
        for p in li:
            li1.append((-p[0],-p[1]))
    elif zn == 5:
        for p in li:
            li1.append((-p[1],-p[0]))
    elif zn == 6:
        for p in li:
            li1.append((p[1],-p[0]))
    elif zn == 7:
        for p in li:
            li1.append((p[0],-p[1]))

    return li1

def do_MPL(x0,y0,x1,y1):
    dx = x1 - x0
    dy = y1 - y0

    if dx == 0 or dy == 0:
        p_li = []
        if dx == 0:
            if dy > 0:
                for y in range(y0, y1+1, 1):
                    p_li.append((x0,y))
            else:
                for y in range(y1, y0+1, 1):
                    p_li.append((x0,y))

        elif dy == 0:
            if dx > 0:
                for x in range(x0, x1+1, 1):
                    p_li.append((x,y0))
            else:
                for x in range(x1, x0+1, 1):
                    p_li.append((x,y0))

        return p_li

    else:
        xa, ya, xb, yb, zn = to_zone_zero(x0,y0,x1,y1)

    dxn = xb - xa
    dyn = yb - ya

    Di = 2*dyn - dxn
    DNE = 2*(dyn - dxn)
    DE = 2*dyn
    D = Di
    
    px_li = [(xa,ya)]

    for x in range(xa+1, xb+1, 1):
        if D > 0:
            D = D + DNE
            ya = ya + 1
            px_li.append((x,ya))
        else:
            D = D + DE
            px_li.append((x,ya))
        
    rev_li = to_zone_prev(px_li, zn)
    return rev_li

def mpl_lines(x0,y0,x1,y1):
    p_li = do_MPL(x0,y0,x1,y1)

    glPointSize(2)
    glBegin(GL_POINTS)

    for p in p_li:
        glVertex2f(p[0],p[1])
    
    glEnd()

def mouse_conv(x,y):
    nx = x
    ny = 700-y
    return (nx,ny)

def mouse_func(button, state, x, y):
    global d_tx, d_lx, d_ly, d_rx, d_ry, d_ty, d_bx, d_by, pause, rc, gc, bc, r, g, b, points, sp, pc
    if state == GLUT_DOWN and button == GLUT_LEFT:
        nx, ny = mouse_conv(x,y)
        
        if (20 <= nx <= 65) and (630 <= ny <= 670):
            if pause == True:
                pause = False
            d_tx = random.randint(20,480)
            d_lx, d_ly, d_rx, d_ry, d_ty, d_bx, d_by = d_tx-10, 600, d_tx+10, 600, 617, d_tx, 583
            r, g, b = random.uniform(0.5,1.0), random.uniform(0.5,1.0), random.uniform(0.5,1.0)
            rc, gc, bc = 1.0, 1.0, 1.0
            points = 0
            sp = 0.125
            pc = 1
            print("Starting Over!")

        elif (235 <= nx <= 270) and (630 <= ny <= 670):
            if pause == False:
                pause = True
            else:
                pause = False
            
        elif (440 <= nx <= 480) and (630 <= ny <= 670):
            glutLeaveMainLoop()
            print('Goodbye, see you!')


def sp_keyL(key,x,y):
    global c_rtx, c_ltx, c_rbx, c_lbx, pause
    if (d_by+16) > 0 and pause == False:
        if key == GLUT_KEY_RIGHT:
            if c_rtx < 480:
                c_rtx += 45
                c_rbx += 45
                c_ltx += 45
                c_lbx += 45
            
        if key == GLUT_KEY_LEFT:
            if c_ltx > 20:
                c_rtx -= 45
                c_rbx -= 45
                c_ltx -= 45
                c_lbx -= 45

    glutPostRedisplay()

def det_collision():
    c1 = (d_rx >= c_ltx and d_rx <= c_rtx)
    c2 = (d_lx <= c_rtx and d_lx >= c_ltx)
    c3 = (d_by <= c_lty and d_by >= c_lby)
    if (c1 or c2) and c3:
        return True
    else:
        return False

def iterate():
    glViewport(0,0,500,700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 700, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    iterate()
    
    global d_tx, d_lx, d_ly, d_rx, d_ry, d_ty, d_bx, d_by, sp, points, r, g, b, rc, gc, bc, pause, pc

    if det_collision():
        sp += 0.025
        points += 1
        print(f"current score: {points}")
        d_tx = random.randint(20,480)
        d_lx, d_ly, d_rx, d_ry, d_ty, d_bx, d_by = d_tx-10, 600, d_tx+10, 600, 617, d_tx, 583
        r, g, b = random.uniform(0.5,1.0), random.uniform(0.5,1.0), random.uniform(0.5,1.0)

    elif (d_by+16) < 0:
        r, g, b = 0.0, 0.0, 0.0
        rc, gc, bc = 1.0, 0.0, 0.0
        if pc == 1:
            print('Oops, Game Over!')
            print(f'your last score: {points}')
            pc = 0
        
    #diamond
    glColor3f(r,g,b)

    mpl_lines(d_lx,d_ly,d_tx,d_ty)
    mpl_lines(d_lx,d_ly,d_bx,d_by)
    mpl_lines(d_rx,d_ry,d_tx,d_ty)
    mpl_lines(d_rx,d_ry,d_bx,d_by)

    #catcher
    glColor3f(rc, gc, bc)

    mpl_lines(c_ltx,c_lty,c_rtx,c_rty)
    mpl_lines(c_ltx,c_lty,c_lbx,c_lby)
    mpl_lines(c_rtx,c_rty,c_rbx,c_rby)
    mpl_lines(c_lbx,c_lby,c_rbx,c_rby)

    #corner_arrow
    glColor3f(0.0,1.0,1.0)

    mpl_lines(20,650,45,670)
    mpl_lines(20,650,45,630)
    mpl_lines(20,650,65,650)

    
    if pause == False:
        #pause_button
        glColor3f(1.0,0.749,0.0)

        mpl_lines(245,670,245,630)
        mpl_lines(255,670,255,630)

    else:
        #play_button
        glColor3f(1.0,0.749,0.0)

        mpl_lines(235,670,235,630)
        mpl_lines(235,670,270,650)
        mpl_lines(235,630,270,650)

    #cross
    glColor3f(1.0,0.0,0.0)

    mpl_lines(480,670,440,630)
    mpl_lines(440,670,480,630)

    glutSwapBuffers()

def animate():
    global d_ty, d_by, d_ry, d_ly, dcr, sp, points, r, g, b, pause

    if (d_by+16) < 0 or pause == True:
        glutPostRedisplay()
        return
    
    else:
        dcr += sp

        if dcr >= 1:
            d_ty = d_ty - 1
            d_by = d_by - 1
            d_ry = d_ry - 1
            d_ly = d_ly - 1
            dcr = 0

        glutPostRedisplay()

#=======================================
glutInit()

glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500,700)
glutInitWindowPosition(0,0)
wind = glutCreateWindow(b"Demo")
glutDisplayFunc(display)
glutSpecialFunc(sp_keyL)
glutMouseFunc(mouse_func)
glutIdleFunc(animate)

glutMainLoop()