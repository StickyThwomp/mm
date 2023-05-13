#ifndef Z_EN_SW_H
#define Z_EN_SW_H

#include "global.h"

struct EnSw;

typedef void (*EnSwActionFunc)(struct EnSw*, PlayState*);

enum EnSw_Type {
    /* 0 */ ENSW_SKULLWALTULA,
    /* 1 */ ENSW_HIDDENGOLD,
    /* 2 */ ENSW_GOLD
};

// Obtain the Skulltula type
#define ENSW_PARAM_GET_TYPE(params) ((params & 3) & 0xFF)
#define ENSW_GET_TYPE(thisx) (ENSW_PARAM_GET_TYPE((thisx)->params))

// Obtain the Chest Flag. (Only applicable for Golden variants)
#define ENSW_PARAM_GET_CHESTFLAG(params) (((params & 0x3FC) >> 2) & 0xFF)
#define ENSW_GET_CHESTFLAG(thisx) (ENSW_PARAM_GET_CHESTFLAG((thisx)->params))

// Obtain the actor's path index.
#define ENSW_GET_PATHIDX(thisx) ((((thisx)->params & 0xFF00) >> 8) & 0xFF)

typedef struct EnSw {
    /* 0x000 */ Actor actor;
    /* 0x144 */ SkelAnime skelAnime;
    /* 0x188 */ EnSwActionFunc actionFunc;
    /* 0x18C */ ColliderSphere collider;
    /* 0x1E4 */ Path* path;
    /* 0x1E8 */ Vec3s jointTable[30];
    /* 0x29C */ Vec3s morphTable[30];
    /* 0x350 */ Vec3f axisForwards;
    /* 0x35C */ Vec3f axisLeft;
    /* 0x368 */ Vec3f axisUp;
    /* 0x374 */ Vec3f targetPosition;
    /* 0x380 */ Vec3f effectOffset[12];
    /* 0x410 */ u16 flags;
    /* 0x412 */ u8 drawDmgEffType;
    /* 0x414 */ f32 distanceToTarget;
    /* 0x418 */ f32 drawDmgEffFrozenSteamScales[12];
    /* 0x448 */ f32 velocityY;
    /* 0x44C */ f32 dashSpeed;
    /* 0x450 */ f32 rotateDirection;
    /* 0x454 */ s16 idleDuration;
    /* 0x456 */ s16 rotateDuration;
    /* 0x458 */ s16 redFilterLife;
    /* 0x45A */ s16 blueFilterLife;
    /* 0x45C */ s16 effectLife;
    /* 0x45E */ s16 stepsToNullRotZ;
    /* 0x460 */ s16 rotationZ;
    /* 0x462 */ s16 numActiveEffects;
    /* 0x464 */ s16 downCountCurrent[12];
    /* 0x47C */ s16 downCountOriginal[12];
    /* 0x494 */ s16 angle;
    /* 0x496 */ s16 targetAngle;
    /* 0x498 */ s16 parentId;
    /* 0x49C */ s32 pathDir;
    /* 0x4A0 */ s32 pathPoint;
} EnSw; // size = 0x4A4

#endif // Z_EN_SW_H
