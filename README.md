# Auto-Clicker with Color Detection

A simple auto-clicker that detects specific colors and automatically clicks when they appear at marked positions.
Used while AFK - away from keyboard 
-this application uses the users mouse directly | might change according to my laziness level

## Features
- Add multiple click points using F8
- Start/Stop monitoring with F6
- Exit application with F7
- Color detection with threshold support
- Visual coordinate list with point locator
- Always-on-top window

## How to Use

1. **Adding Click Points**
   - Move your cursor to desired location
   - Press F8 to add the point
   - You can add multiple points

2. **Starting the Auto-Clicker**
   - Press F6 to start monitoring
   - The program will check for color RGB(156, 194, 255) at marked positions
   - When color is detected, it will automatically click
   - Press F6 again to stop

3. **Managing Points**
   - Use the "Clear Points" button to remove all points
   - Click the arrow (→) next to any point to locate it
   - Points are saved until cleared or program is closed

4. **Exiting the Program**
   - Press F7 or close the window to exit

## Notes
- The program looks for color RGB(156, 194, 255) with a threshold of 50
- Points cannot be added while monitoring is active
- Make sure to run as administrator if clicking in elevated windows

## Troubleshooting
- If clicks aren't working in some applications, try running as administrator
- Make sure the target color is visible (not covered by other windows)
- The program needs all files in this folder to run properly
