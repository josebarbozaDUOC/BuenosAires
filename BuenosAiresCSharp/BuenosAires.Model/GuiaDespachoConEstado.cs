namespace BuenosAires.Model
{
    using System;
    using System.Collections.Generic;

    public partial class GuiaDespachoConEstado
    {
        public int nrogd { get; set; }
        public string producto { get; set; }
        public string fechagd { get; set; }
        public string estadogd { get; set; }
        public int nrofac { get; set; }
        public string cliente { get; set; }

    }
}