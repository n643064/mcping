CPP=g++
CXXFLAGS=-Wall -fpermissive -std=c++17
LFLAGS=
OBJ=main.o
TARGET=mcping

default: clean run

clean:
	rm -f *.o $(TARGET)

%.o: %.cpp
	$(CPP) $(CXXFLAGS) -c $^ -o $@

$(TARGET): $(OBJ)
	$(CPP) $(OBJ) -o $(TARGET) $(LFLAGS)

run: $(TARGET)
	./$(TARGET) 127.0.0.1 25565
