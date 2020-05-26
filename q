[1mdiff --git a/lib/states/Connecting.py b/lib/states/Connecting.py[m
[1mindex 9e6d118..3f394fa 100644[m
[1m--- a/lib/states/Connecting.py[m
[1m+++ b/lib/states/Connecting.py[m
[36m@@ -24,7 +24,6 @@[m [mclass Connecting(States):[m
         while Globals.connection.inputs:[m
             player_input = Globals.connection.get_input()[m
             if player_input.new_game:[m
[31m-                self.done = True[m
                 self.switch('server game')[m
                 Globals.connection.add_input(player_input)[m
                 break[m
[1mdiff --git a/lib/states/Level_Selection_Menu.py b/lib/states/Level_Selection_Menu.py[m
[1mindex 2a16d48..5e0fa20 100644[m
[1m--- a/lib/states/Level_Selection_Menu.py[m
[1m+++ b/lib/states/Level_Selection_Menu.py[m
[36m@@ -45,8 +45,6 @@[m [mclass Level_Selection_Menu(States):[m
                     Globals.connection.add_input(player_input)[m
                     self.switch('client game')[m
 [m
[31m-                    self.done = True[m
[31m-[m
     def draw(self, screen):[m
         screen.fill((150, 150, 150))[m
 [m
[1mdiff --git a/lib/states/Pause_Menu.py b/lib/states/Pause_Menu.py[m
[1mindex 029c78c..687417e 100644[m
[1m--- a/lib/states/Pause_Menu.py[m
[1m+++ b/lib/states/Pause_Menu.py[m
[36m@@ -27,8 +27,6 @@[m [mclass Pause_Menu(States):[m
                     Globals.connection.add_input(player_input)[m
                     self.switch('client game')[m
 [m
[31m-                self.done = True[m
[31m-[m
     def draw(self, screen):[m
         screen.fill((150, 150, 150))[m
         title_string = 'Pause'[m
[1mdiff --git a/lib/states/ServerGame.py b/lib/states/ServerGame.py[m
[1mindex da759a4..c096c6e 100644[m
[1m--- a/lib/states/ServerGame.py[m
[1m+++ b/lib/states/ServerGame.py[m
[36m@@ -17,8 +17,6 @@[m [mclass ServerGame(States):[m
 [m
         States.__init__(self)[m
 [m
[31m-        self.next = 'connecting'[m
[31m-[m
         self.state = GameState()[m
 [m
         self.das_threshold = 0[m
[36m@@ -66,8 +64,8 @@[m [mclass ServerGame(States):[m
     def do_event(self, event):[m
 [m
         if event.type == pygame.QUIT:[m
[31m-            self.done = True[m
[31m-[m
[32m+[m[32m            self.switch('connecting')[m
[32m+[m[41m            [m
         if event.type == pygame.KEYDOWN:[m
             if event.key == pygame.K_BACKQUOTE:[m
                 pdb.set_trace()[m
[36m@@ -321,7 +319,6 @@[m [mclass ServerGame(States):[m
                 self.state.game_over = True[m
                 Globals.connection.set_state(self.state)[m
                 self.switch('connecting')[m
[31m-                self.done = True[m
 [m
         Globals.connection.set_state(self.state)[m
 [m
