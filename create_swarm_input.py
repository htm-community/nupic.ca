import csv
import automatatron

BITS = 21

with open("swarm_description.tmpl", "r") as swarm_desc_tmpl:
  swarm_desc = swarm_desc_tmpl.read()
  incl_fields = []
  midpoint = BITS / 2
  for i in xrange(BITS):
    incl_fields.append(dict(
      fieldName="bit_%i" % i,
      fieldType="string"
    ))
  swarm_desc = swarm_desc.replace("<INCLUDED_FIELDS>", str(incl_fields))
  swarm_desc = swarm_desc.replace("<PREDICTED_FIELD>", "bit_%i" % midpoint)
  with open("swarm_description.py", "w") as swarm_desc_out:
    swarm_desc_out.write(swarm_desc)


with open("swarm_input.csv", "w") as input_file:
  writer = csv.writer(input_file)
  names = []
  types = []
  flags = []
  for i in xrange(BITS):
    names.append("bit_%i" % i)
    types.append("string")
    flags.append("")
  writer.writerow(names)
  writer.writerow(types)
  writer.writerow(flags)


  automaton = automatatron.Engine(30)
  def stream_handler(row, _):
    writer.writerow(row)


  automaton.run(iterations=BITS)

  automaton.run(handler=stream_handler, width=BITS, iterations=3000)
