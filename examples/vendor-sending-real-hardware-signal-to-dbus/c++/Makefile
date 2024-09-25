# Makefile for compiling send_signal using D-Bus

# Compiler and flags
CXX = g++
CXXFLAGS = $(shell pkg-config --cflags dbus-1)
LDFLAGS = $(shell pkg-config --libs dbus-1)

# Target executable
TARGET = send_signal
SRC = send_signal.cpp

# Default rule
all: $(TARGET)

# Rule to compile the target
$(TARGET): $(SRC)
	$(CXX) -o $(TARGET) $(SRC) $(CXXFLAGS) $(LDFLAGS)

# Clean rule to remove the compiled binary
clean:
	rm -f $(TARGET)
