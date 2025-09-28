def bytes_to_human(n):
	"""Convert bytes to human-readable string."""
	symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i * 10)
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return f'{value:.1f} {s}'
	return f"{n} B"
