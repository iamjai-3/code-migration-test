const { data } = require("../data/data");

const getItems = (req, res) => {
  const { id } = req.params;

  if (id) {
    const item = data[parseInt(id)];
    if (item) {
      return res.json(item);
    }
    return res.status(404).json({ message: "Item not found" });
  }

  return res.json(Object.values(data));
};

const createItem = (req, res) => {
  const { name, description } = req.body;
  const id = Object.keys(data).length + 1;

  data[id] = { id, name, description };
  return res.status(201).json(data[id]);
};

const updateItem = (req, res) => {
  const { id } = req.params;
  const { name, description } = req.body;

  if (!data[id]) {
    return res.status(404).json({ message: "Item not found" });
  }

  data[id] = {
    ...data[id],
    name: name || data[id].name,
    description: description || data[id].description,
  };

  return res.json(data[id]);
};

const deleteItem = (req, res) => {
  const { id } = req.params;

  if (!data[id]) {
    return res.status(404).json({ message: "Item not found" });
  }

  delete data[id];
  return res.json({ message: "Item deleted" });
};

module.exports = {
  getItems,
  createItem,
  updateItem,
  deleteItem,
};
