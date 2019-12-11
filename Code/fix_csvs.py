import re

# Some of the captions were over multiple lines which made it impossible to load them properly in Spark.

for year in range(2013, 2020):
	loc = "tomorrowland_Posts_" + str(year) + ".csv"
	out = "posts_" + str(year) + ".csv"

	f = open(loc, "r")
	g = open(out, "w")

	for line in f:
		# If the line doesn't end properly, it's not supposed to be the end of the line.
		if not re.findall(r".*;(False|True|Is_video)\n", line):
			g.write(line[:-1])
		else:
			g.write(line[:])

	f.close()
	g.close()


