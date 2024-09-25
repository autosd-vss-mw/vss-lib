# Makefile for D-Bus hardware signal program

CC = gcc
CFLAGS = -Wall
LIBS = `pkg-config --cflags --libs dbus-1`
TARGET = send_signal

# Default target
all: $(TARGET)

# Compile the program
$(TARGET): send_signal.o
	$(CC) $(CFLAGS) -o $(TARGET) send_signal.o $(LIBS)

# Compile object file
send_signal.o: send_signal.c
	$(CC) $(CFLAGS) -c send_signal.c $(LIBS)

# Clean up build files
clean:
	rm -f *.o $(TARGET)

.PHONY: all clean
