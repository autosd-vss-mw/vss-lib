golang$ go mod init send_signal
golang$ go mod tidy
golang$ go get github.com/godbus/dbus/v5
golang$ go build -o send_signal main.go

$ sudo ./send_signal
Hardware signal 'Speed' with value 80.000000 sent to D-Bus.
Signal sent successfully.
