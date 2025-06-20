const fastify = require("fastify")({ logger: false });
const http = require("http");
const socketIO = require("socket.io");

fastify.get("/", (req, reply) => {
  reply.send("🟢 Servidor Reveal.js Multiplex activo");
});

const server = http.createServer(fastify);
const io = socketIO(server, {
  cors: { origin: "*" }
});

let clients = {};

io.on("connection", (socket) => {
  socket.on("multiplex-register", (data) => {
    clients[data.secret] = true;
  });

  socket.on("multiplex-statechanged", (data) => {
    if (data.secret && clients[data.secret]) {
      socket.broadcast.emit("multiplex-statechanged", data);
    }
  });

  socket.on("disconnect", () => {
    for (let secret in clients) {
      delete clients[secret];
    }
  });
});

server.listen(process.env.PORT || 3000, "0.0.0.0", () => {
  console.log("✅ Servidor multiplex corriendo");
});
