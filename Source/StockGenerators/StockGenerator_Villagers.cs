using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using Verse;

namespace AnimalCrossingVillagers {
    public class StockGenerator_Villagers : StockGenerator {
        public override IEnumerable<Thing> GenerateThings()
        {
            StringBuilder sb = new StringBuilder();
            List<Thing> things = new List<Thing>();
            //ThingDef thingDef = DefDatabase<ThingDef>.GetNamed("Human");

            for(int i = 0; i < RandomCountOf(PawnKindDefOf.Slave.race); i++)
            {
                Thing thing = PawnGenerator.GeneratePawn(PawnKindDefOf.Slave, Faction.OfColony);
                things.Add(thing);
                sb.AppendLine(thing.Label);
                Log.Message("thing:" + thing.ThingID);
            }

            Log.Message("StockGenerator_Animals:");
            Log.Message(sb.ToString());
            return things as IEnumerable<Thing>;
        }
    }

}