import pythonosc.osc_server
import pythonosc.dispatcher

def main():
	def on_osc_message(addr, args):
		print(addr, args)

	dispatcher = pythonosc.dispatcher.Dispatcher()
	dispatcher.set_default_handler(on_osc_message)

	server = pythonosc.osc_server.ThreadingOSCUDPServer(
		('0.0.0.0', 11543),
		dispatcher
	)
	server.serve_forever()

if __name__ == '__main__':
	main()
