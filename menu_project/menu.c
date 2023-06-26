#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <string.h>

// Constants for color attributes
#define COLOR_DEFAULT 7
#define COLOR_SELECTED 10

char password[100]; // Declare password variable
char escapedPassword[200]; // Declare escapedPassword variable

void setColor(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

void setFontSize(int size) {
    CONSOLE_FONT_INFOEX fontInfo;
    fontInfo.cbSize = sizeof(CONSOLE_FONT_INFOEX);
    GetCurrentConsoleFontEx(GetStdHandle(STD_OUTPUT_HANDLE), FALSE, &fontInfo);
    fontInfo.dwFontSize.X = size;
    fontInfo.dwFontSize.Y = size;
    SetCurrentConsoleFontEx(GetStdHandle(STD_OUTPUT_HANDLE), FALSE, &fontInfo);
}

void printBoxedText(const char* text) {
    int textLength = strlen(text);
    int boxWidth = textLength + 4;  // Add padding of 2 on each side

    // Print top border
    printf("+");
    for (int i = 0; i < boxWidth; i++) {
        printf("-");
    }
    printf("+\n");

    // Print text with side borders
    printf("|  %s  |\n", text);

    // Print bottom border
    printf("+");
    for (int i = 0; i < boxWidth; i++) {
        printf("-");
    }
    printf("+\n");
}

void printOption(const char* option, int isSelected) {
    if (isSelected) {
        setColor(COLOR_SELECTED);
        printf(">> %s\n", option);
        setColor(COLOR_DEFAULT);
    } else {
        printf("   %s\n", option);
    }
}

void goodbyeMessage() {
    system("cls");  // Clear console screen
    printf("Thank you for using the AWS Login Manager!\n");
    printf("Goodbye!\n");
    Sleep(2000);  // Pause for 2 seconds before exiting
}

void escapeSpecialCharacters(char* password) {
    int len = strlen(password);
    char escapedPassword[len * 2 + 1];
    int j = 0;

    for (int i = 0; i < len; i++) {
        switch (password[i]) {
            case '^':
            case '&':
            case '<':
            case '>':
            case '|':
            case '%':
            case '!':
            case '(':
            case ')':
            case '[':
            case ']':
            case '{':
            case '}':
            case ',':
            case ';':
            case '=':
            case '+':
            case '-':
            case '*':
            case '?':
            case '~':
                escapedPassword[j++] = '^';
                break;
        }
        escapedPassword[j++] = password[i];
    }

    escapedPassword[j] = '\0';
    strcpy(password, escapedPassword);
}

void maskPassword(char* password) {
    int len = strlen(password);
    for (int i = 0; i < len; i++) {
        password[i] = '*';
    }
}

void login(char* password) {
    printf("\nOption 1 selected: Login\n");
    printf("Enter your password: ");

    int i = 0;
    char ch;

    // Mask the password with asterisks
    while ((ch = getch()) != '\r') {  // Read characters until Enter is pressed
        if (ch == '\b' && i > 0) {
            // Handle backspace: erase previous character
            printf("\b \b");
            i--;
        } else {
            password[i++] = ch;
            printf("*");
        }
    }
    password[i] = '\0';  // Null-terminate the password string

    escapeSpecialCharacters(password);  // Escape special characters in the password

    printf("\nPress any key to return to the main menu...");
    getch();  // Wait for any key press
}

int main() {
    const char* welcomeText = "Welcome to the AWS Login Manager";
    const char* options[] = {
        "1. Login",
        "2. Switch Accounts",
        "3. Exit"
    };
    int numOptions = sizeof(options) / sizeof(options[0]);

    int currentOption = 0;
    int keyPressed;

    setFontSize(16);  // Set the default font size to 16

    do {
        system("cls");  // Clear console screen

        // Print title box
        printBoxedText(welcomeText);

        printf("\n");  // Add space between title and options

        // Print options
        for (int i = 0; i < numOptions; i++) {
            printOption(options[i], i == currentOption);
        }

        // Wait for keypress
        keyPressed = getch();

        // Process arrow key input
        if (keyPressed == 0 || keyPressed == 224) {
            switch (getch()) {
                case 72:  // Up arrow
                    currentOption = (currentOption - 1 + numOptions) % numOptions;
                    break;
                case 80:  // Down arrow
                    currentOption = (currentOption + 1) % numOptions;
                    break;
            }
        }
    } while (keyPressed != 13);  // 13 is the ASCII code for Enter key

    // Perform action based on the selected option
    switch (currentOption) {
        case 0: {
            login(password);
            break;
        }
        case 1: {
            printf("\nOption 2 selected: Switch Accounts\n");

            // Create the directory name using the escaped password
            char directoryName[100];
            sprintf(directoryName, "dir_%s", password);

            // Print the command
            printf("Command: mkdir %s\n", directoryName);

            printf("Creating directory using the escaped password...\n");

            // Execute the mkdir command with the escaped password as an argument
            char command[100];
            sprintf(command, "mkdir %s", directoryName);
            system(command);

            printf("Directory created!\n");

            printf("\nPress any key to return to the main menu...");
            getch();  // Wait for any key press
            break;
        }
        case 2:
            printf("\nOption 3 selected: Exit\n");
            goodbyeMessage();
            return 0;
    }

    // Return to the main menu
    main();
}
