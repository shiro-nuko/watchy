#ifndef WATCHY_POKEMON_H
#define WATCHY_POKEMON_H

#define SIM
//#define FR

#ifdef SIM
#include "..\..\Watchy.h"
#else
#include <Watchy.h>
#include "wta.h"
#endif

#include "FreeMonoBold10pt7b.h"
#include "FreeMonoBold7pt7b.h"

#ifdef FR
#include "pokemon_fr.h"
#else
#include "pokemon.h"
#endif

#ifdef SIM
class WatchyPokemon : public Watchy
#else
class WatchyPokemon : public WatchySynced
#endif
{
#ifndef SIM
    using WatchySynced::WatchySynced;
#endif
public:
    void drawWatchFace();
    double randomDay(uint32_t d);
    double randomHour(uint32_t d);
    double randomMinute(uint32_t d);
};

#endif
