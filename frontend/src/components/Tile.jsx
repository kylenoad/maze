const Tile = (props) => (
  <div
    style={{
      display: "inline-block",
      width: 30,
      height: 30,
      textAlign: "center",
      border: "1px solid #ccc",
    }}
  >
    {props.isPlayer ? "🧍" : props.cell || "\u00A0"}
  </div>
);

export default Tile;
