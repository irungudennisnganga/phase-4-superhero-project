import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

function Hero() {
  const [{ data: hero, error, status }, setHero] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();

  useEffect(() => {
    fetch(`/heroes/${id}`)
      .then((r) => r.json())
      .then((hero) => setHero({ data: hero, error: null, status: "resolved" }))
      .catch((err) => setHero({ data: null, error: err.message, status: "rejected" }));
  }, [id]);
  // console.log(hero)
  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error}</h1>;

  return (
    <section>
      <h2>{hero.super_name}</h2>
      <h2>AKA {hero.name}</h2>

      <h3>Powers:</h3>
      <ul>
        {
          hero.heropowers.map((power) => (
            <li key={power.id}>
              <Link to={`/powers/${power.id}`}>{power.power.name}</Link>
            </li>
          ))}
         
      {/* //     <li>No powers listed.</li> */}
        
       </ul>

      <Link to="/hero_powers/new">Add Hero Power</Link>
    </section>
  );
}

export default Hero;
