/*
 * File: z_en_sw.c
 * Overlay: ovl_En_Sw
 * Description: Skullwalltula
 */

#include "z_en_sw.h"
#include "objects/object_st/object_st.h"

#define FLAGS (ACTOR_FLAG_1 | ACTOR_FLAG_4)

#define THIS ((EnSw*)thisx)

enum EnSw_Flags {
    ENSW_FLAG_0 = (1 << 0),
    ENSW_FLAG_1 = (1 << 1), // Potentially the blue fire effect around the token after being destroyed?
    ENSW_FLAG_2 = (1 << 2),
    ENSW_FLAG_3 = (1 << 3),
    ENSW_FLAG_4 = (1 << 4),
    ENSW_FLAG_5 = (1 << 5)

};

enum EnSw_MoveControl { DONT_MOVE = 0, DO_MOVE = 1 };

void EnSw_Init(Actor* thisx, PlayState* play);
void EnSw_Destroy(Actor* thisx, PlayState* play);
void EnSw_Update(Actor* thisx, PlayState* play);
void EnSw_Draw(Actor* thisx, PlayState* play);

void EnSw_WaitForProximity(EnSw* this, PlayState* play);
void EnSw_Dash(EnSw* this, PlayState* play);
void Action_NOT_FLAG5_808DA578(EnSw* this, PlayState* play);
void Action_FLAG5_808DA6FC(EnSw* this, PlayState* play);
void EnSw_Attacked(EnSw* this, PlayState* play);
void EnSw_FollowPath(EnSw* this, PlayState* play);
void EnSw_DashOnPath(EnSw* this, PlayState* play);
void EnSw_Death(EnSw* this, PlayState* play);
void EnSw_Rotate(EnSw* this, PlayState* play);
void EnSw_Cutscene(EnSw* this, PlayState* play);
void EnSw_Idle(EnSw* this, PlayState* play);

ActorInit En_Sw_InitVars = {
    ACTOR_EN_SW,
    ACTORCAT_NPC,
    FLAGS,
    OBJECT_ST,
    sizeof(EnSw),
    (ActorFunc)EnSw_Init,
    (ActorFunc)EnSw_Destroy,
    (ActorFunc)EnSw_Update,
    (ActorFunc)EnSw_Draw,
};

static ColliderSphereInit sSphereInit = {
    {
        COLTYPE_NONE,
        AT_ON | AT_TYPE_ENEMY,
        AC_ON | AC_TYPE_PLAYER,
        OC1_ON | OC1_TYPE_ALL,
        OC2_TYPE_1,
        COLSHAPE_SPHERE,
    },
    {
        ELEMTYPE_UNK0,
        { 0xF7CFFFFF, 0x00, 0x00 },
        { 0xF7CFFFFF, 0x00, 0x00 },
        TOUCH_ON | TOUCH_SFX_NORMAL,
        BUMP_ON,
        OCELEM_ON,
    },
    { 0, { { 0, 0, 0 }, 16 }, 100 },
};

static CollisionCheckInfoInit2 sColChkInfoInit = { 1, 0, 0, 0, MASS_IMMOVABLE };

static DamageTable sDamageTable = {
    /* Deku Nut       */ DMG_ENTRY(1, 0x0),
    /* Deku Stick     */ DMG_ENTRY(1, 0x0),
    /* Horse trample  */ DMG_ENTRY(0, 0x0),
    /* Explosives     */ DMG_ENTRY(1, 0x0),
    /* Zora boomerang */ DMG_ENTRY(1, 0x0),
    /* Normal arrow   */ DMG_ENTRY(1, 0x0),
    /* UNK_DMG_0x06   */ DMG_ENTRY(0, 0x0),
    /* Hookshot       */ DMG_ENTRY(1, 0x0),
    /* Goron punch    */ DMG_ENTRY(1, 0x0),
    /* Sword          */ DMG_ENTRY(1, 0x0),
    /* Goron pound    */ DMG_ENTRY(2, 0x0),
    /* Fire arrow     */ DMG_ENTRY(2, 0x2),
    /* Ice arrow      */ DMG_ENTRY(2, 0x3),
    /* Light arrow    */ DMG_ENTRY(2, 0x4),
    /* Goron spikes   */ DMG_ENTRY(1, 0x0),
    /* Deku spin      */ DMG_ENTRY(1, 0x0),
    /* Deku bubble    */ DMG_ENTRY(1, 0x0),
    /* Deku launch    */ DMG_ENTRY(2, 0x0),
    /* UNK_DMG_0x12   */ DMG_ENTRY(1, 0x0),
    /* Zora barrier   */ DMG_ENTRY(1, 0x5),
    /* Normal shield  */ DMG_ENTRY(1, 0x0),
    /* Light ray      */ DMG_ENTRY(1, 0x0),
    /* Thrown object  */ DMG_ENTRY(1, 0x0),
    /* Zora punch     */ DMG_ENTRY(1, 0x0),
    /* Spin attack    */ DMG_ENTRY(1, 0x0),
    /* Sword beam     */ DMG_ENTRY(0, 0x0),
    /* Normal Roll    */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1B   */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1C   */ DMG_ENTRY(0, 0x0),
    /* Unblockable    */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1E   */ DMG_ENTRY(0, 0x0),
    /* Powder Keg     */ DMG_ENTRY(1, 0x0),
};

static CollisionCheckInfoInit2 sColChkInfoInit2 = { 1, 0, 0, 0, MASS_IMMOVABLE };

static DamageTable sDamageTable2 = {
    /* Deku Nut       */ DMG_ENTRY(0, 0x1),
    /* Deku Stick     */ DMG_ENTRY(1, 0x0),
    /* Horse trample  */ DMG_ENTRY(0, 0x0),
    /* Explosives     */ DMG_ENTRY(1, 0x0),
    /* Zora boomerang */ DMG_ENTRY(1, 0x0),
    /* Normal arrow   */ DMG_ENTRY(1, 0x0),
    /* UNK_DMG_0x06   */ DMG_ENTRY(0, 0x0),
    /* Hookshot       */ DMG_ENTRY(1, 0x0),
    /* Goron punch    */ DMG_ENTRY(1, 0x0),
    /* Sword          */ DMG_ENTRY(1, 0x0),
    /* Goron pound    */ DMG_ENTRY(2, 0x0),
    /* Fire arrow     */ DMG_ENTRY(2, 0x2),
    /* Ice arrow      */ DMG_ENTRY(2, 0x3),
    /* Light arrow    */ DMG_ENTRY(2, 0x4),
    /* Goron spikes   */ DMG_ENTRY(1, 0x0),
    /* Deku spin      */ DMG_ENTRY(1, 0x0),
    /* Deku bubble    */ DMG_ENTRY(1, 0x0),
    /* Deku launch    */ DMG_ENTRY(2, 0x0),
    /* UNK_DMG_0x12   */ DMG_ENTRY(0, 0x1),
    /* Zora barrier   */ DMG_ENTRY(1, 0x5),
    /* Normal shield  */ DMG_ENTRY(1, 0x0),
    /* Light ray      */ DMG_ENTRY(1, 0x0),
    /* Thrown object  */ DMG_ENTRY(1, 0x0),
    /* Zora punch     */ DMG_ENTRY(1, 0x0),
    /* Spin attack    */ DMG_ENTRY(1, 0x0),
    /* Sword beam     */ DMG_ENTRY(0, 0x0),
    /* Normal Roll    */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1B   */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1C   */ DMG_ENTRY(0, 0x0),
    /* Unblockable    */ DMG_ENTRY(0, 0x0),
    /* UNK_DMG_0x1E   */ DMG_ENTRY(0, 0x0),
    /* Powder Keg     */ DMG_ENTRY(1, 0x0),
};

static AnimationInfoS sAnimationInfo[] = {
    { &object_st_Anim_000304, 1.0f, 0, -1, ANIMMODE_ONCE_INTERP, 0 },
    { &object_st_Anim_000304, 1.0f, 0, -1, ANIMMODE_ONCE_INTERP, -4 },
    { &object_st_Anim_0055A8, 1.0f, 0, -1, ANIMMODE_LOOP_INTERP, -4 },
    { &object_st_Anim_005B98, 1.0f, 0, -1, ANIMMODE_LOOP_INTERP, -4 },
};

void EnSw_SpawnDust(EnSw* this, PlayState* play) {
    static Color_RGBA8 sEnSwDustPrimColor = { 170, 130, 90, 255 };
    static Color_RGBA8 sEnSwDustEnvColor = { 100, 60, 20, 0 };
    s32 i;
    Vec3f velocity;
    Vec3f accel;
    Vec3f pos;
    Vec3f temp;
    s32 life;
    s16 rotAngle;

    rotAngle = (Rand_ZeroOne() - 0.5f) * 0x10000;
    pos.y = this->actor.floorHeight;

    for (i = 0; i < 8; i++, rotAngle += 0x1FFE) {
        life = (Rand_ZeroOne() * 4.0f) + 8.0f;

        temp.x = 0.0f;
        temp.y = (Rand_ZeroOne() * 0.2f) + 0.1f;
        temp.z = Rand_ZeroOne() + 1.0f;
        Lib_Vec3f_TranslateAndRotateY(&gZeroVec3f, rotAngle, &temp, &accel);

        temp.x = 0.0f;
        temp.y = 0.7f;
        temp.z = 2.0f;
        Lib_Vec3f_TranslateAndRotateY(&gZeroVec3f, rotAngle, &temp, &velocity);

        pos.x = this->actor.world.pos.x + (2.0f * velocity.x);
        pos.z = this->actor.world.pos.z + (2.0f * velocity.z);
        func_800B0EB0(play, &pos, &velocity, &accel, &sEnSwDustPrimColor, &sEnSwDustEnvColor, 60, 30, life);
    }
}

s32 EnSw_SetEffects(EnSw* this) {
    s16 effectAngle = (s16)((s16)(Rand_ZeroOne() * 1000.0f) % ARRAY_COUNT(this->downCountCurrent)) * 0x1555;
    s32 i;

    for (i = 0; i < ARRAY_COUNT(this->downCountCurrent); i++, effectAngle += 0x1555) { // += 30 deg.
        if (this->drawDmgEffType != ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX) {
            this->downCountCurrent[i] = (Rand_ZeroOne() * 16.0f) + 8.0f;
        } else {
            this->downCountCurrent[i] = 80;
        }
        this->downCountOriginal[i] = this->downCountCurrent[i];
        this->drawDmgEffFrozenSteamScales[i] = 0.45000002f;
        if ((this->drawDmgEffType == ACTOR_DRAW_DMGEFF_FIRE) || (this->drawDmgEffType == ACTOR_DRAW_DMGEFF_BLUE_FIRE) ||
            (this->drawDmgEffType == ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX)) {
            this->effectOffset[i].y = (Rand_ZeroOne() - 0.5f) * 20.0f;
        } else {
            this->effectOffset[i].y = ((Rand_ZeroOne() - 0.5f) * 20.0f) + 10.0f;
        }
        this->effectOffset[i].x = Math_SinS(effectAngle) * 10.0f;
        this->effectOffset[i].z = Math_CosS(effectAngle) * 10.0f;
    }
    this->numActiveEffects = 1;
    return 0;
}

s32 EnSw_DrawDamageEffects(EnSw* this, PlayState* play, s32 arg2) {
    s32 ret = false;
    u8 drawDmgEffType;
    Vec3f limbPos[1];
    f32 drawDmgEffAlpha;

    if (arg2 < this->numActiveEffects) {
        if (this->downCountCurrent[arg2] != 0) {
            drawDmgEffAlpha = (f32)this->downCountCurrent[arg2] / this->downCountOriginal[arg2];
            drawDmgEffType = this->drawDmgEffType;
            Math_ApproachF(&this->drawDmgEffFrozenSteamScales[arg2], 0.3f, 0.3f, 0.5f);
            Math_Vec3f_Copy(&limbPos[0], &this->actor.world.pos);
            limbPos[0].x += this->effectOffset[arg2].x;
            limbPos[0].y += this->effectOffset[arg2].y;
            limbPos[0].z += this->effectOffset[arg2].z;
            if (drawDmgEffType == ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX) {
                if ((this->downCountOriginal[arg2] - this->downCountCurrent[arg2]) < 20) {
                    drawDmgEffType = ACTOR_DRAW_DMGEFF_FROZEN_SFX;
                }
                drawDmgEffAlpha = 1.0f;
            }
            Actor_DrawDamageEffects(play, &this->actor, limbPos, ARRAY_COUNT(limbPos), 0.3f,
                                    this->drawDmgEffFrozenSteamScales[arg2], drawDmgEffAlpha, drawDmgEffType);
            ret = true;
        }
    }
    return ret;
}

void EnSw_SpawnIceEffects(EnSw* this, PlayState* play) {
    Vec3f position;
    s32 i;

    for (i = 0; i < ARRAY_COUNT(this->effectOffset); i++) {
        Math_Vec3f_Copy(&position, &this->actor.world.pos);
        position.x += this->effectOffset[i].x;
        position.y += this->effectOffset[i].y;
        position.z += this->effectOffset[i].z;
        Math_Vec3f_Copy(&this->effectOffset[i], &position);
    }
    Actor_SpawnIceEffects(play, &this->actor, this->effectOffset, ARRAY_COUNT(this->effectOffset), 3, 0.1f, 0.3f);
}

void EnSw_PerformCollisionChecks(EnSw* this, PlayState* play) {
    Math_Vec3f_ToVec3s(&this->collider.dim.worldSphere.center, &this->actor.world.pos);
    this->collider.dim.worldSphere.radius = this->collider.dim.modelSphere.radius * this->collider.dim.scale;
    if (!(this->flags & ENSW_FLAG_4) && (this->actor.colChkInfo.health != 0) && (DECR(this->redFilterLife) <= 10)) {
        CollisionCheck_SetAC(play, &play->colChkCtx, &this->collider.base);
    }

    if (!(this->flags & ENSW_FLAG_4) && (this->actor.colChkInfo.health != 0)) {
        CollisionCheck_SetAT(play, &play->colChkCtx, &this->collider.base);
    }

    if (this->flags & ENSW_FLAG_2) {
        CollisionCheck_SetOC(play, &play->colChkCtx, &this->collider.base);
    }
}

s32 EnSw_ApplyDamage(EnSw* this) {
    if (this->actor.colChkInfo.damage < this->actor.colChkInfo.health) {
        this->actor.colChkInfo.health -= this->actor.colChkInfo.damage;
    } else {
        this->actor.colChkInfo.health = 0;
    }
    return this->actor.colChkInfo.health;
}

void EnSw_RotateToTarget(EnSw* this, s32 isGradual, s16 angle) {
    Vec3f newForwardVector;
    s16 previousAngle;
    s16 delta;

    if (isGradual == true) {
        previousAngle = this->angle;
        Math_ApproachS(&this->angle, this->targetAngle, 4, 0xE38);
        delta = this->angle - previousAngle;
    } else {
        delta = angle;
    }

    Matrix_RotateAxisF(BINANG_TO_RAD_ALT(delta), &this->axisUp, MTXMODE_NEW);
    Matrix_MultVec3f(&this->axisForwards, &newForwardVector);
    Math_Vec3f_Copy(&this->axisForwards, &newForwardVector);
    Math3D_CrossProduct(&this->axisUp, &this->axisForwards, &this->axisLeft);
}

// Returns True if the Floor Poly is valid for the Skullwalltula to move on, false otherwise.
s32 EnSw_UpdateFloorPoly(EnSw* this, CollisionPoly* floorPoly) {
    f32 angle;
    f32 normDotUp;
    f32 magnitude;
    Vec3f normal;
    Vec3f vecLeft;

    this->actor.floorPoly = floorPoly;
    if (floorPoly != NULL) {
        normal.x = COLPOLY_GET_NORMAL(floorPoly->normal.x);
        normal.y = COLPOLY_GET_NORMAL(floorPoly->normal.y);
        normal.z = COLPOLY_GET_NORMAL(floorPoly->normal.z);
    } else {
        return false;
    }

    normDotUp = DOTXYZ(normal, this->axisUp);
    if (fabsf(normDotUp) >= 0.999f) {
        return false;
    }

    angle = Math_FAcosF(normDotUp);
    if (angle < 0.001f) {
        return false;
    }

    Math3D_CrossProduct(&this->axisUp, &normal, &vecLeft);

    magnitude = Math3D_Vec3fMagnitude(&vecLeft);
    if (magnitude < 0.001f) {
        return false;
    }

    Math_Vec3f_Scale(&vecLeft, 1.0f / magnitude);
    Matrix_RotateAxisF(angle, &vecLeft, MTXMODE_NEW);
    Matrix_MultVec3f(&this->axisLeft, &vecLeft);
    Math_Vec3f_Copy(&this->axisLeft, &vecLeft);
    Math3D_CrossProduct(&this->axisLeft, &normal, &this->axisForwards);

    magnitude = Math3D_Vec3fMagnitude(&this->axisForwards);
    if (magnitude < 0.001f) {
        return false;
    }

    Math_Vec3f_Scale(&this->axisForwards, 1.0f / magnitude);
    Math_Vec3f_Copy(&this->axisUp, &normal);

    return true;
}

/**
 * @brief Update the actor's rotation based on the local object rotational Axes.
 *
 * @see EnSw_UpdateAxesFromActorRot for the inverse.
 */
void EnSw_UpdateRotationFromAxes(EnSw* this) {
    MtxF rotMatrix;

    rotMatrix.xx = this->axisLeft.x;
    rotMatrix.yx = this->axisLeft.y;
    rotMatrix.zx = this->axisLeft.z;
    rotMatrix.xy = this->axisUp.x;
    rotMatrix.yy = this->axisUp.y;
    rotMatrix.zy = this->axisUp.z;
    rotMatrix.xz = this->axisForwards.x;
    rotMatrix.yz = this->axisForwards.y;
    rotMatrix.zz = this->axisForwards.z;
    Matrix_MtxFToYXZRot(&rotMatrix, &this->actor.world.rot, false);
    this->actor.world.rot.x = -this->actor.world.rot.x;
}

s32 EnSw_IsOnCollisionPoly(PlayState* play, Vec3f* posA, Vec3f* posB, Vec3f* posResult, CollisionPoly** outPoly,
                           s32* bgId) {
    s32 ret = false;

    if (BgCheck_EntityLineTest1(&play->colCtx, posA, posB, posResult, outPoly, true, true, true, true, bgId) &&
        !(SurfaceType_GetWallFlags(&play->colCtx, *outPoly, *bgId) & (WALL_FLAG_4 | WALL_FLAG_5))) {
        ret = true;
    }
    return ret;
}

void EnSw_RotateAndMove(EnSw* this, PlayState* play, s32 doMove, s32 isGradual, s16 angle) {
    CollisionPoly* polySide = NULL;
    CollisionPoly* polyUpDown = NULL;
    s32 isFloorPolyValid;
    Vec3f positionA;
    Vec3f positionB;
    Vec3f posSide;
    Vec3f posUpDown;

    s32 bgIdUpDown = BGCHECK_SCENE;
    s32 bgIdSide = BGCHECK_SCENE;

    Actor* thisx = &this->actor;
    f32 lineLength;
    s32 i;

    EnSw_RotateToTarget(this, isGradual, angle);

    thisx->speed = this->dashSpeed;
    lineLength = 2.0f * thisx->speed;

    positionA.x = thisx->world.pos.x + (this->axisUp.x * 2.0f);
    positionA.y = thisx->world.pos.y + (this->axisUp.y * 2.0f);
    positionA.z = thisx->world.pos.z + (this->axisUp.z * 2.0f);

    positionB.x = thisx->world.pos.x - (this->axisUp.x * 4.0f);
    positionB.y = thisx->world.pos.y - (this->axisUp.y * 4.0f);
    positionB.z = thisx->world.pos.z - (this->axisUp.z * 4.0f);

    if (EnSw_IsOnCollisionPoly(play, &positionA, &positionB, &posUpDown, &polyUpDown, &bgIdUpDown)) {
        // Forwards
        positionB.x = (this->axisForwards.x * lineLength) + positionA.x;
        positionB.y = (this->axisForwards.y * lineLength) + positionA.y;
        positionB.z = (this->axisForwards.z * lineLength) + positionA.z;

        if (EnSw_IsOnCollisionPoly(play, &positionA, &positionB, &posSide, &polySide, &bgIdSide)) {
            isFloorPolyValid = EnSw_UpdateFloorPoly(this, polySide);
            Math_Vec3f_Copy(&thisx->world.pos, &posSide);
            thisx->floorBgId = bgIdSide;
            thisx->speed = 0.0f;
        } else {
            if (polyUpDown != thisx->floorPoly) {
                isFloorPolyValid = EnSw_UpdateFloorPoly(this, polyUpDown);
            }

            Math_Vec3f_Copy(&thisx->world.pos, &posUpDown);
            thisx->floorBgId = bgIdUpDown;
        }
    } else {

        thisx->speed = 0.0f;
        lineLength *= 3.0f;
        Math_Vec3f_Copy(&positionA, &positionB);

        for (i = 0; i < 3; i++) {

            if (i == 0) {
                // Backwards
                positionB.x = positionA.x - (this->axisForwards.x * lineLength);
                positionB.y = positionA.y - (this->axisForwards.y * lineLength);
                positionB.z = positionA.z - (this->axisForwards.z * lineLength);

            } else if (i == 1) {
                // Left
                positionB.x = positionA.x + (this->axisLeft.x * lineLength);
                positionB.y = positionA.y + (this->axisLeft.y * lineLength);
                positionB.z = positionA.z + (this->axisLeft.z * lineLength);

            } else {
                // Right
                positionB.x = positionA.x - (this->axisLeft.x * lineLength);
                positionB.y = positionA.y - (this->axisLeft.y * lineLength);
                positionB.z = positionA.z - (this->axisLeft.z * lineLength);
            }

            if (EnSw_IsOnCollisionPoly(play, &positionA, &positionB, &posSide, &polySide, &bgIdSide)) {
                isFloorPolyValid = EnSw_UpdateFloorPoly(this, polySide);
                Math_Vec3f_Copy(&thisx->world.pos, &posSide);
                thisx->floorBgId = bgIdSide;
                break;
            }
        }

        //! FAKE
        if (i == 3) {
            // No collision
        }
    }

    if (true || isFloorPolyValid) {
        EnSw_UpdateRotationFromAxes(this);
        thisx->shape.rot.x = -thisx->world.rot.x;
        thisx->shape.rot.y = thisx->world.rot.y;
        thisx->shape.rot.z = thisx->world.rot.z;
    }

    if (thisx->speed != 0.0f) {
        this->dashSpeed = thisx->speed;
    }

    if (doMove == true) {
        Actor_MoveWithoutGravity(&this->actor);
    }
}

void EnSw_ApplyTransform(EnSw* this, Vec3f* vec) {
    Vec3f relative;
    MtxF transform;

    transform.xx = this->axisLeft.x;
    transform.xy = this->axisLeft.y;
    transform.xz = this->axisLeft.z;
    transform.xw = 0.0f;

    transform.yx = this->axisUp.x;
    transform.yy = this->axisUp.y;
    transform.yz = this->axisUp.z;
    transform.yw = 0.0f;

    transform.zx = this->axisForwards.x;
    transform.zy = this->axisForwards.y;
    transform.zz = this->axisForwards.z;
    transform.zw = 0.0f;

    transform.wx = 0.0f;
    transform.wy = 0.0f;
    transform.wz = 0.0f;
    transform.ww = 0.0f;

    Matrix_Put(&transform);
    relative.x = vec->x - this->actor.world.pos.x;
    relative.y = vec->y - this->actor.world.pos.y;
    relative.z = vec->z - this->actor.world.pos.z;
    Matrix_MultVec3f(&relative, vec);
}

s32 func_808D9968(EnSw* this, PlayState* play) {
    s32 ret = false;
    s32 chestFlag = ENSW_GET_CHESTFLAG(&this->actor);

    if (ENSW_GET_TYPE(&this->actor)) {
        if ((chestFlag != 0x3F) && Flags_GetTreasure(play, chestFlag)) {
            ret = true;
        }
    }

    return ret;
}

s32 EnSw_DidHitPlayer(EnSw* this, PlayState* play) {
    s32 phi_v1 = 0;

    if (ENSW_GET_TYPE(&this->actor) || (this->redFilterLife > 10) || (this->actor.colChkInfo.health == 0)) {
        return false;
    }

    if ((this->actor.xyzDistToPlayerSq < ((sREG(16) * 10) + 60000)) && (play->actorCtx.playerImpact.timer != 0) &&
        (play->actorCtx.playerImpact.type == PLAYER_IMPACT_GORON_GROUND_POUND)) {
        this->actor.colChkInfo.damage = 4;
        phi_v1 = true;
    }

    return phi_v1;
}

s32 EnSw_AnimateAndPlaySound(EnSw* this, PlayState* play) {
    s16 angle = 0;
    f32 frame;

    if (DECR(this->idleDuration) == 0) {
        if (!Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame)) {
            frame = this->skelAnime.endFrame - this->skelAnime.curFrame;
            angle = (80.0f * frame) * this->rotateDirection;
        } else {
            if (this->rotateDuration != 0) {
                if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA)) {
                    Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_ROLL);
                } else {
                    Actor_PlaySfx(&this->actor, NA_SE_EN_STALGOLD_ROLL);
                }
                this->rotateDuration--;
                this->skelAnime.curFrame = 0.0f;
            } else {
                this->idleDuration = Rand_S16Offset(20, 20);
                this->rotateDuration = (Rand_ZeroOne() * 10.0f) + 3.0f;
            }

            if (this->rotateDuration % 2) {
                if (Rand_ZeroOne() < 0.5f) {
                    this->rotateDirection = -1.0f;
                } else {
                    this->rotateDirection = 1.0f;
                }
            }
        }
        EnSw_RotateAndMove(this, play, DONT_MOVE, false, angle);
    }

    return false;
}

s32 EnSw_Spawn(EnSw* this) {
    Vec3f sp3C;
    Vec3f sp30;
    f32 new_var;

    if ((this->parentId == 0xF9) || (this->parentId == 0x82) || (this->parentId == 0xE4) || (this->parentId == 0xE5)) {
        this->actor.velocity.x = this->actor.speed;
        this->actor.velocity.z = this->actor.speed;
        this->actor.velocity.x *= Math_SinS(this->actor.world.rot.y);
        this->actor.velocity.z *= Math_CosS(this->actor.world.rot.y);
    } else {
        new_var = this->actor.speed * this->axisForwards.x;
        this->actor.velocity.x = new_var + (this->actor.speed * this->axisUp.x);
        new_var = this->actor.speed * this->axisForwards.z;
        this->actor.velocity.z = new_var + this->actor.speed * this->axisUp.z;
        this->actor.velocity.y = 14.0f;
        Math_Vec3f_Copy(&sp3C, &this->actor.world.pos);
        Math_Vec3f_Copy(&sp30, &this->actor.world.pos);
        sp30.x += this->actor.velocity.x;
        sp30.y += this->actor.velocity.y;
        sp30.z += this->actor.velocity.z;
        this->actor.world.rot.x = 0;
        this->actor.world.rot.z = 0;
        this->actor.world.rot.y = Math_Vec3f_Yaw(&sp3C, &sp30);
    }

    Actor_PlaySfx(&this->actor, NA_SE_EN_STALTURA_APPEAR);

    if (ENSW_GET_TYPE(&this->actor) == 1) {
        // Is Gold
        Actor_SetScale(&this->actor, 0.0f);
        this->actor.world.rot.x = 0;
        this->actor.world.rot.z = 0;
        Math_Vec3s_Copy(&this->actor.shape.rot, &this->actor.world.rot);
        this->flags |= ENSW_FLAG_2;
    }

    this->actor.gravity = -1.4f;
    this->actor.parent = NULL;
    return false;
}

/**
 * @brief Update the axes of rotation based on the actor's rotation angles.
 *
 * @see EnSw_UpdateRotationFromAxes for the inverse.
 */
void EnSw_UpdateAxesFromActorRot(EnSw* this) {
    static Vec3f sUnitVectY = { 0.0f, 1.0f, 0.0f };
    s32 pad;
    MtxF rotationMatrix;

    SkinMatrix_SetRotateYRP(&rotationMatrix, this->actor.shape.rot.x, this->actor.shape.rot.y, this->actor.shape.rot.z);
    SkinMatrix_Vec3fMtxFMultXYZ(&rotationMatrix, &sUnitVectY, &this->axisUp);

    this->axisForwards.x = Math_SinS(this->actor.shape.rot.y);
    this->axisForwards.y = 0.0f;
    this->axisForwards.z = Math_CosS(this->actor.shape.rot.y);

    this->axisLeft.x = Math_SinS(BINANG_ADD(this->actor.shape.rot.y, 0x4000));
    this->axisLeft.y = 0.0f;
    this->axisLeft.z = Math_CosS(BINANG_ADD(this->actor.shape.rot.y, 0x4000));
}

void EnSw_HandleAttackedMovement(EnSw* this) {
    Vec3f sp1C;

    this->actor.shape.rot.z = -0x8000;
    this->actor.shape.rot.x = 0;
    this->actor.shape.rot.y = 0;
    Math_Vec3s_Copy(&this->actor.world.rot, &this->actor.shape.rot);
    this->actor.gravity = -1.4f;
    this->actor.velocity.y = 0.0f;
    this->rotateDuration = 2;

    Math_Vec3f_Copy(&sp1C, &this->actor.world.pos);
    sp1C.x += this->axisUp.x * 16.0f;
    sp1C.y += this->axisUp.y * 16.0f;
    sp1C.z += this->axisUp.z * 16.0f;
    Math_Vec3f_Copy(&this->actor.world.pos, &sp1C);
}

void EnSw_InitializeForPathing(EnSw* this) {
    this->idleDuration = Rand_S16Offset(20, 20);
    this->rotateDuration = (Rand_ZeroOne() * 10.0f) + 3.0f;
    this->distanceToTarget = 0.0f;
    this->stepsToNullRotZ = this->rotationZ;
}

void EnSw_InitVisible(EnSw* this, PlayState* play, s32 arg2) {
    if (arg2 != 0) {
        func_800BC154(play, &play->actorCtx, &this->actor, 5);
    }
    Actor_SetScale(&this->actor, 0.02f);
    EnSw_UpdateAxesFromActorRot(this);

    this->actor.speed = 10.0f;
    this->dashSpeed = 10.0f;
    EnSw_RotateAndMove(this, play, DONT_MOVE, false, 0);
    this->actor.speed = 0.0f;
    this->dashSpeed = 0.0f;

    this->rotateDirection = 1.0f;
    Math_Vec3f_Copy(&this->actor.home.pos, &this->actor.world.pos);
    this->flags |= ENSW_FLAG_2;
}

void func_808DA024(EnSw* this, PlayState* play) {
    EnSw_UpdateAxesFromActorRot(this);

    this->actor.speed = 10.0f;
    this->dashSpeed = 10.0f;
    EnSw_RotateAndMove(this, play, DONT_MOVE, false, 0);
    this->actor.speed = 0.0f;
    this->dashSpeed = 0.0f;

    this->rotateDirection = 1.0f;
}

s32 EnSw_HandleAttack(EnSw* this, PlayState* play) {
    s32 ret = 0;
    s32 i;

    if (EnSw_DidHitPlayer(this, play) || (this->collider.base.acFlags & AC_HIT)) {
        this->collider.base.acFlags &= ~AC_HIT;

        if (this->actor.colChkInfo.damageEffect == 4) {
            Actor_Spawn(&play->actorCtx, play, ACTOR_EN_CLEAR_TAG, this->actor.world.pos.x, this->actor.world.pos.y,
                        this->actor.world.pos.z, 0, 0, 0, CLEAR_TAG_LARGE_LIGHT_RAYS);
        }

        if (this->drawDmgEffType == ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX) {
            // clang-format off
            for (i = 0; i < ARRAY_COUNT(this->downCountCurrent); i++) { this->downCountCurrent[i] = 0; }
            // clang-format on

            this->effectLife = 0;
        } else if (!EnSw_ApplyDamage(this)) {
            SoundSource_PlaySfxAtFixedWorldPos(play, &this->actor.world.pos, 40, NA_SE_EN_STALTU_DEAD);
            Enemy_StartFinishingBlow(play, &this->actor);
            this->actor.flags &= ~ACTOR_FLAG_1;
            if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA)) {
                SubS_ChangeAnimationByInfoS(&this->skelAnime, sAnimationInfo, 3);
            }

            switch (this->actor.colChkInfo.damageEffect) {
                case 4:
                    this->drawDmgEffType = ACTOR_DRAW_DMGEFF_LIGHT_ORBS;
                    this->effectLife = 20;
                    EnSw_SetEffects(this);
                    break;

                case 3:
                    this->drawDmgEffType = ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX;
                    this->effectLife = 0;
                    EnSw_SetEffects(this);
                    break;

                case 2:
                    this->drawDmgEffType = ACTOR_DRAW_DMGEFF_FIRE;
                    this->effectLife = 20;
                    EnSw_SetEffects(this);
                    break;

                case 5:
                    this->drawDmgEffType = ACTOR_DRAW_DMGEFF_ELECTRIC_SPARKS_SMALL;
                    this->effectLife = 20;
                    EnSw_SetEffects(this);
                    break;

                default:
                    this->drawDmgEffType = ACTOR_DRAW_DMGEFF_BLUE_FIRE;
                    this->effectLife = 0;
                    break;
            }

            if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA) &&
                (this->drawDmgEffType != ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX)) {
                EnSw_HandleAttackedMovement(this);
            }
            this->redFilterLife = 20;
            this->blueFilterLife = 0;
            Actor_SetColorFilter(&this->actor, COLORFILTER_COLORFLAG_RED, 200, COLORFILTER_BUFFLAG_OPA,
                                 this->redFilterLife);
            ret = true;
        } else if (this->actor.colChkInfo.damageEffect == 1) {
            if (this->blueFilterLife == 0) {
                Actor_PlaySfx(&this->actor, NA_SE_EN_COMMON_FREEZE);
                this->blueFilterLife = 40;
                Actor_SetColorFilter(&this->actor, COLORFILTER_COLORFLAG_BLUE, 200, COLORFILTER_BUFFLAG_OPA,
                                     this->blueFilterLife);
            }
        } else {
            Actor_PlaySfx(&this->actor, NA_SE_EN_STALTU_DAMAGE);
            this->redFilterLife = 20;
            this->blueFilterLife = 0;
            Actor_SetColorFilter(&this->actor, COLORFILTER_COLORFLAG_RED, 200, COLORFILTER_BUFFLAG_OPA,
                                 this->redFilterLife);
        }
    }
    return ret;
}

void EnSw_WaitForProximity(EnSw* this, PlayState* play) {
    Player* player = GET_PLAYER(play);

    if ((player->stateFlags1 & PLAYER_STATE1_200000) && (this->actor.xyzDistToPlayerSq < 8000.0f)) {
        Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_LAUGH);
        Math_Vec3f_Copy(&this->targetPosition, &player->actor.world.pos);
        this->flags &= ~ENSW_FLAG_5;
        this->distanceToTarget = 0.0f;
        this->actionFunc = EnSw_Dash;
    } else {
        EnSw_AnimateAndPlaySound(this, play);
    }
}

void EnSw_Dash(EnSw* this, PlayState* play) {
    s16 rotationToTarget;
    s16 minDashAngle = 0;
    Vec3f targetPosition;
    f32 framesRemaining;

    if (!Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame)) {
        // If not done rotating
        framesRemaining = this->skelAnime.endFrame - this->skelAnime.curFrame;
        minDashAngle = (s16)(80.0f * framesRemaining);
        Math_Vec3f_Copy(&targetPosition, &this->targetPosition);
        EnSw_ApplyTransform(this, &targetPosition);
        rotationToTarget = Math_Atan2S_XY(targetPosition.z, targetPosition.x);

        if (ABS_ALT(rotationToTarget) < minDashAngle) {
            // Rotation target is within range, perform the dash.
            this->skelAnime.curFrame = 0.0f;
            Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_DASH);
            this->distanceToTarget = 0.0f;
            if (this->flags & ENSW_FLAG_5) {
                this->actionFunc = Action_FLAG5_808DA6FC;
            } else {
                this->actionFunc = Action_NOT_FLAG5_808DA578;
            }

            minDashAngle = ABS_ALT(rotationToTarget);
        }

        // Assign proper polarity
        minDashAngle *= (rotationToTarget < 0) ? -1 : 1;
    } else {
        Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_ROLL);
        this->skelAnime.curFrame = 0.0f;
    }

    EnSw_RotateAndMove(this, play, DONT_MOVE, false, minDashAngle);
}

void Action_NOT_FLAG5_808DA578(EnSw* this, PlayState* play) {
    f32 framesRemaining;
    f32 distanceToTarget;
    s16 rotationToTarget;
    Vec3f targetPosition;

    if (!Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame)) {
        framesRemaining = this->skelAnime.endFrame - this->skelAnime.curFrame;
        this->dashSpeed = 0.3f * framesRemaining;
        EnSw_RotateAndMove(this, play, DO_MOVE, false, 0);
        if ((this->actor.speed == 0.0f) && (this->dashSpeed != 0.0f)) {
            // Move
            Math_Vec3f_Copy(&targetPosition, &this->targetPosition);
            EnSw_ApplyTransform(this, &targetPosition);
            rotationToTarget = Math_Atan2S_XY(targetPosition.z, targetPosition.x);
            EnSw_RotateAndMove(this, play, DONT_MOVE, false, rotationToTarget);
        }
    } else if (this->flags & ENSW_FLAG_5) {
        Math_Vec3f_Copy(&this->targetPosition, &this->actor.home.pos);
        this->actionFunc = EnSw_Dash;
    } else {
        Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_DASH);
        this->skelAnime.curFrame = 0.0f;
    }

    distanceToTarget = Math_Vec3f_DistXYZ(&this->actor.world.pos, &this->targetPosition);
    if (!(this->flags & ENSW_FLAG_5) && ((s32)this->distanceToTarget != 0) &&
        ((s32)this->distanceToTarget < (s32)distanceToTarget)) {
        this->flags |= ENSW_FLAG_5;
    }
    this->distanceToTarget = distanceToTarget;
}

/**
 *
 */
void Action_FLAG5_808DA6FC(EnSw* this, PlayState* play) {
    f32 sp4C;
    f32 framesRemaining;
    s16 rotationToTarget;
    Vec3f targetPosition;

    if (!Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame)) {
        // Animate
        framesRemaining = this->skelAnime.endFrame - this->skelAnime.curFrame;
        this->dashSpeed = 0.14f * framesRemaining;
        EnSw_RotateAndMove(this, play, DO_MOVE, false, 0);
        if ((this->actor.speed == 0.0f) && (this->dashSpeed != 0.0f)) {
            Math_Vec3f_Copy(&targetPosition, &this->targetPosition);
            EnSw_ApplyTransform(this, &targetPosition);
            rotationToTarget = Math_Atan2S_XY(targetPosition.z, targetPosition.x);
            EnSw_RotateAndMove(this, play, DONT_MOVE, false, rotationToTarget);
        }
    } else {
        Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_DASH);
        this->skelAnime.curFrame = 0.0f;
    }

    sp4C = Math_Vec3f_DistXYZ(&this->actor.world.pos, &this->targetPosition);

    if (((s32)this->distanceToTarget != 0) && ((s32)this->distanceToTarget < (s32)sp4C)) {
        Math_Vec3f_Copy(&this->actor.world.pos, &this->targetPosition);
        this->idleDuration = Rand_S16Offset(20, 20);
        this->rotateDuration = (Rand_ZeroOne() * 10.0f) + 3.0f;
        this->actionFunc = EnSw_WaitForProximity;
        this->skelAnime.curFrame = 0.0f;
    }
    this->distanceToTarget = sp4C;
}

void EnSw_Attacked(EnSw* this, PlayState* play) {
    if (this->drawDmgEffType == ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX) {
        s32 i;
        s32 count;
        s16 phi_a0;

        for (i = 0, count = 0; i < ARRAY_COUNT(this->downCountCurrent); i++) {
            if (this->downCountCurrent[i] == 0) {
                phi_a0 = 0;
            } else {
                this->downCountCurrent[i]--;
                phi_a0 = this->downCountCurrent[i];
            }
            if (phi_a0 == 0) {
                count++;
            }
        }

        if (count == ARRAY_COUNT(this->downCountCurrent)) {
            if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA)) {
                EnSw_HandleAttackedMovement(this);
            }
            this->drawDmgEffType = ACTOR_DRAW_DMGEFF_BLUE_FIRE;
            EnSw_SpawnIceEffects(this, play);
        }
    } else if (ENSW_GET_TYPE(&this->actor)) {
        this->actionFunc = EnSw_Death;
    } else {
        if (this->actor.bgCheckFlags & BGCHECKFLAG_GROUND) {
            f32 newVelocityY;

            this->actor.shape.yOffset = 400.0f;
            newVelocityY = fabsf(this->actor.velocity.y) * 0.6f;
            this->actor.velocity.y = newVelocityY;
            this->velocityY = newVelocityY;
            this->actor.speed = 0.0f;
            if ((s32)newVelocityY != 0) {
                Actor_PlaySfx(&this->actor, NA_SE_EN_STALTURA_BOUND);
            } else {
                this->actionFunc = EnSw_Death;
                this->actor.velocity.y = 0.0f;
            }
            if ((s32)this->actor.velocity.y >= 2) {
                EnSw_SpawnDust(this, play);
            }
        } else {
            Math_ApproachF(&this->actor.shape.yOffset, 400.0f, 0.3f, 1000.0f);
        }

        Actor_MoveWithGravity(&this->actor);
        Actor_UpdateBgCheckInfo(play, &this->actor, 30.0f, 12.0f, 0.0f, UPDBGCHECKINFO_FLAG_4);
    }
}

void EnSw_FollowPath(EnSw* this, PlayState* play) {
    Vec3s* pathPoints;
    s16 rotationToTarget;
    s16 minDashAngle;
    Vec3f targetPos;
    f32 framesRemaining;

    pathPoints = Lib_SegmentedToVirtual(this->path->points);
    minDashAngle = 0;

    if (DECR(this->idleDuration) == 0) {
        if (Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame) == 0) {
            framesRemaining = this->skelAnime.endFrame - this->skelAnime.curFrame;
            minDashAngle = 80.0f * framesRemaining;
            if (this->stepsToNullRotZ == 0) {
                Math_Vec3s_ToVec3f(&targetPos, &pathPoints[this->pathPoint]);
                EnSw_ApplyTransform(this, &targetPos);
                rotationToTarget = Math_Atan2S_XY(targetPos.z, targetPos.x);
                if (ABS_ALT(rotationToTarget) < minDashAngle) {
                    this->skelAnime.curFrame = 0.0f;
                    Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_DASH);
                    Math_Vec3s_ToVec3f(&this->targetPosition, &pathPoints[this->pathPoint]);
                    this->actionFunc = EnSw_DashOnPath;
                    this->distanceToTarget = 0.0f;
                    minDashAngle = ABS_ALT(rotationToTarget);
                }
                minDashAngle *= (rotationToTarget < 0) ? -1 : 1;
            }
        } else {
            if (this->rotateDuration != 0) {
                Actor_PlaySfx(&this->actor, NA_SE_EN_STALGOLD_ROLL);
                this->rotateDuration--;
                this->skelAnime.curFrame = 0.0f;
            } else {
                this->idleDuration = Rand_S16Offset(20, 20);
                this->rotateDuration = (Rand_ZeroOne() * 10.0f) + 3.0f;
                if (this->stepsToNullRotZ != 0) {
                    this->stepsToNullRotZ--;
                }
            }

            if (this->rotateDuration % 2) {
                if (Rand_ZeroOne() < 0.5f) {
                    this->rotateDirection = -1.0f;
                } else {
                    this->rotateDirection = 1.0f;
                }
            }
        }
    }
    EnSw_RotateAndMove(this, play, DONT_MOVE, false, minDashAngle);
}

void EnSw_DashOnPath(EnSw* this, PlayState* play) {
    f32 distanceToTarget;
    f32 framesRemaining;
    s16 rotationToTarget;

    if (Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame) == 0) {
        Vec3f targetPosition;

        framesRemaining = this->skelAnime.endFrame - this->skelAnime.curFrame;
        this->dashSpeed = 0.1f * framesRemaining;
        EnSw_RotateAndMove(this, play, DO_MOVE, false, 0);
        if ((this->actor.speed == 0.0f) && (this->dashSpeed != 0.0f)) {

            Math_Vec3f_Copy(&targetPosition, &this->targetPosition);
            EnSw_ApplyTransform(this, &targetPosition);
            rotationToTarget = Math_Atan2S_XY(targetPosition.z, targetPosition.x);
            EnSw_RotateAndMove(this, play, DONT_MOVE, false, rotationToTarget);
        }
    } else {
        Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_DASH);
        this->skelAnime.curFrame = 0.0f;
    }

    distanceToTarget = Math_Vec3f_DistXYZ(&this->actor.world.pos, &this->targetPosition);

    if (((s32)this->distanceToTarget != 0) && ((s32)this->distanceToTarget < (s32)distanceToTarget)) {
        // Snap to target and select the next path point
        Math_Vec3f_Copy(&this->actor.world.pos, &this->targetPosition);
        this->pathPoint += this->pathDir;
        if ((this->pathPoint >= this->path->count) || (this->pathPoint < 0)) {
            // Reverse direction.
            this->pathDir = -this->pathDir;
            this->pathPoint += this->pathDir * 2;
        }

        if (this->flags & ENSW_FLAG_3) {
            EnSw_InitializeForPathing(this);
            this->actionFunc = EnSw_FollowPath;
        } else {
            this->actionFunc = EnSw_Rotate;
        }
    }
    this->distanceToTarget = distanceToTarget;
}

void EnSw_Death(EnSw* this, PlayState* play) {
    Vec3f position;
    s32 i;
    s32 count;
    s16 phi_a0;

    if (this->flags & ENSW_FLAG_1) {
        if (ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA) {
            if (this->flags & ENSW_FLAG_2) {
                phi_a0 = DECR(this->effectLife);
                if (phi_a0 == 0) {
                    this->flags &= ~ENSW_FLAG_2;
                }
            }

            for (i = 0, count = 0; i < ARRAY_COUNT(this->downCountCurrent); i++) {
                if (this->downCountCurrent[i] == 0) {
                    phi_a0 = 0;
                } else {
                    this->downCountCurrent[i]--;
                    phi_a0 = this->downCountCurrent[i];
                }
                if (phi_a0 == 0) {
                    count++;
                }
            }

            if (count == ARRAY_COUNT(this->downCountCurrent)) {
                Actor_Kill(&this->actor);
            }
        } else {
            // Diminish and spawn Gold Skultulla Token.
            Math_ApproachF(&this->actor.scale.x, 0.0f, 0.08f, 1.0f);
            Actor_SetScale(&this->actor, this->actor.scale.x);
            if ((s32)(this->actor.scale.x * 100.0f) == 0) {

                Math_Vec3f_Copy(&position, &this->actor.world.pos);
                position.x += this->axisUp.x * 10.0f;
                position.y += this->axisUp.y * 10.0f;
                position.z += this->axisUp.z * 10.0f;
                if (Actor_SpawnAsChild(&play->actorCtx, &this->actor, play, ACTOR_EN_SI, position.x, position.y,
                                       position.z, 0, 0, 0, this->actor.params) != NULL) {
                    play_sound(NA_SE_SY_KINSTA_MARK_APPEAR);
                }
                Actor_Kill(&this->actor);
            }
            EnSw_RotateAndMove(this, play, DONT_MOVE, false, 0x1554);
        }
    } else {
        phi_a0 = DECR(this->effectLife);
        if (phi_a0 == 0) {
            this->flags |= ENSW_FLAG_1;
            if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA) &&
                (this->drawDmgEffType == ACTOR_DRAW_DMGEFF_BLUE_FIRE)) {
                EnSw_SetEffects(this);
                this->effectLife = 10;
            } else {
                this->effectLife = 20;
            }
        }
    }
}

void EnSw_Rotate(EnSw* this, PlayState* play) {
    if (this->actor.parent != NULL) {
        this->parentId = this->actor.parent->id;
        this->rotateDuration = 0;
        this->idleDuration = 0;
        this->skelAnime.curFrame = 0.0f;
        func_800BC154(play, &play->actorCtx, &this->actor, 4);
        this->actionFunc = EnSw_Cutscene;
        return;
    }

    if (!(this->flags & ENSW_FLAG_0)) {
        EnSw_AnimateAndPlaySound(this, play);
        return;
    }

    if ((DECR(this->idleDuration) == 0) && Animation_OnFrame(&this->skelAnime, this->skelAnime.endFrame)) {
        if (this->rotateDuration != 0) {
            // Play sound when rotating
            if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA)) {
                Actor_PlaySfx(&this->actor, NA_SE_EN_STALWALL_ROLL);
            } else {
                Actor_PlaySfx(&this->actor, NA_SE_EN_STALGOLD_ROLL);
            }
            this->rotateDuration--;
            this->skelAnime.curFrame = 0.0f;
        } else {
            // When paused between rotations, seed the next rotation.
            this->idleDuration = Rand_S16Offset(20, 20);
            this->rotateDuration = (Rand_ZeroOne() * 10.0f) + 3.0f;
        }
    }
}

void EnSw_Cutscene(EnSw* this, PlayState* play) {
    if (CutsceneManager_GetCurrentCsId() == CS_ID_GLOBAL_TALK) {
        CutsceneManager_Stop(CS_ID_GLOBAL_TALK);
    } else if (CutsceneManager_IsNext(this->actor.csId)) {
        CutsceneManager_StartWithPlayerCs(this->actor.csId, &this->actor);
        EnSw_Spawn(this);
        this->actionFunc = EnSw_Idle;
    } else {
        CutsceneManager_Queue(this->actor.csId);
    }
}

void EnSw_Idle(EnSw* this, PlayState* play) {
    f32 newVelocityY;

    if (this->actor.bgCheckFlags & BGCHECKFLAG_GROUND) {
        EnSw_InitVisible(this, play, 0);
        newVelocityY = fabsf(this->actor.velocity.y) * 0.6f;
        this->actor.velocity.x *= 0.5f;
        this->actor.velocity.y = newVelocityY;
        this->velocityY = newVelocityY;
        this->actor.velocity.z *= 0.5f;

        if ((s32)newVelocityY != 0) {
            Actor_PlaySfx(&this->actor, NA_SE_EN_STALTURA_BOUND);
        } else {
            func_800BC154(play, &play->actorCtx, &this->actor, 5);
            Math_Vec3f_Copy(&this->actor.velocity, &gZeroVec3f);
            this->flags &= ~(ENSW_FLAG_4 | ENSW_FLAG_0);
            this->actionFunc = EnSw_Rotate;
        }

        if ((s32)this->actor.velocity.y >= 2) {
            EnSw_SpawnDust(this, play);
        }
    }

    Math_ApproachF(&this->actor.scale.x, 0.02f, 0.4f, 1.0f);
    Actor_SetScale(&this->actor, this->actor.scale.x);
    this->actor.velocity.y += this->actor.gravity;
    Actor_UpdatePos(&this->actor);
    Actor_UpdateBgCheckInfo(play, &this->actor, 30.0f, 12.0f, 0.0f, UPDBGCHECKINFO_FLAG_4);
}

void EnSw_Init(Actor* thisx, PlayState* play) {
    EnSw* this = THIS;
    s32 pad;

    if (!func_808D9968(this, play)) {
        ActorShape_Init(&this->actor.shape, 0.0f, NULL, 0.0f);
        SkelAnime_Init(play, &this->skelAnime, &object_st_Skel_005298, NULL, this->jointTable, this->morphTable, 30);
        SubS_ChangeAnimationByInfoS(&this->skelAnime, sAnimationInfo, 0);
        this->skelAnime.playSpeed = 4.0f;

        Collider_InitAndSetSphere(play, &this->collider, &this->actor, &sSphereInit);
        if ((ENSW_GET_TYPE(&this->actor) == ENSW_SKULLWALTULA)) {
            this->actor.hintId = TATL_HINT_ID_SKULLWALLTULA;
            CollisionCheck_SetInfo2(&this->actor.colChkInfo, &sDamageTable, &sColChkInfoInit);
            this->collider.info.toucher.damage = 8;
        } else {
            this->actor.hintId = TATL_HINT_ID_GOLD_SKULLTULA;
            CollisionCheck_SetInfo2(&this->actor.colChkInfo, &sDamageTable2, &sColChkInfoInit2);
            this->collider.info.toucher.damage = 16;
        }

        this->path = SubS_GetDayDependentPath(play, ENSW_GET_PATHIDX(&this->actor), 255, &this->pathPoint);
        if (this->path != NULL) {
            this->pathPoint = 1;
        }

        switch (ENSW_GET_TYPE(&this->actor)) {
            case ENSW_SKULLWALTULA:
                EnSw_InitVisible(this, play, 1);
                this->actionFunc = EnSw_WaitForProximity;
                break;

            case ENSW_HIDDENGOLD:
                this->actor.flags &= ~ACTOR_FLAG_1;
                this->actor.flags |= ACTOR_FLAG_10;

                if (this->actor.world.rot.z < 0) {
                    this->rotationZ = -thisx->world.rot.z;
                } else {
                    this->rotationZ = thisx->world.rot.z;
                }

                if (this->actor.world.rot.z >= 0) {
                    this->flags |= ENSW_FLAG_3;
                }

                func_808DA024(this, play);
                this->flags |= (ENSW_FLAG_4 | ENSW_FLAG_0);
                this->flags &= ~ENSW_FLAG_2;
                this->actionFunc = EnSw_Rotate;
                break;

            case ENSW_GOLD:
            case 3:
                this->actor.flags &= ~ACTOR_FLAG_1;
                this->actor.flags |= ACTOR_FLAG_10;

                if (this->actor.world.rot.z < 0) {
                    this->rotationZ = -thisx->world.rot.z;
                } else {
                    this->rotationZ = thisx->world.rot.z;
                }

                if (this->actor.world.rot.z >= 0) {
                    this->flags |= ENSW_FLAG_3;
                }

                EnSw_InitVisible(this, play, 1);
                if (this->path != NULL) {
                    this->pathDir = 1;
                    EnSw_InitializeForPathing(this);
                    this->actionFunc = EnSw_FollowPath;
                } else {
                    this->actionFunc = EnSw_Rotate;
                }
                break;
        }
    } else {
        Actor_Kill(&this->actor);
    }
}

void EnSw_Destroy(Actor* thisx, PlayState* play) {
    EnSw* this = THIS;

    Collider_DestroySphere(play, &this->collider);
}

void EnSw_Update(Actor* thisx, PlayState* play) {
    EnSw* this = THIS;

    if (EnSw_HandleAttack(this, play)) {
        this->actionFunc = EnSw_Attacked;
    } else if (DECR(this->blueFilterLife) == 0) {
        this->actionFunc(this, play);
    }

    if ((this->drawDmgEffType != ACTOR_DRAW_DMGEFF_FROZEN_NO_SFX) || (this->blueFilterLife != 0)) {
        SkelAnime_Update(&this->skelAnime);
    }

    Actor_SetFocus(&this->actor, 0.0f);
    EnSw_PerformCollisionChecks(this, play);
}

/**
 * Override the actors limbs when this is a Gold Skultula
 */
s32 EnSw_OverrideLimbDraw(PlayState* play, s32 limbIndex, Gfx** dList, Vec3f* pos, Vec3s* rot, Actor* thisx) {
    EnSw* this = THIS;

    if (ENSW_GET_TYPE(&this->actor) != ENSW_SKULLWALTULA) {
        switch (limbIndex) {
            case 23:
                *dList = object_st_DL_004788;
                break;

            case 8:
                *dList = object_st_DL_0046F0;
                break;

            case 14:
                *dList = object_st_DL_004658;
                break;

            case 11:
                *dList = object_st_DL_0045C0;
                break;

            case 26:
                *dList = object_st_DL_004820;
                break;

            case 20:
                *dList = object_st_DL_0048B8;
                break;

            case 17:
                *dList = object_st_DL_004950;
                break;

            case 29:
                *dList = object_st_DL_0049E8;
                break;

            case 5:
                *dList = object_st_DL_003FB0;
                break;

            case 4:
                *dList = object_st_DL_0043D8;
                break;
        }
    }
    return false;
}

void EnSw_Draw(Actor* thisx, PlayState* play) {
    EnSw* this = THIS;
    s32 i;
    s32 count;

    if (this->flags & ENSW_FLAG_2) {
        if (ENSW_GET_TYPE(&this->actor)) {
            func_800B8050(&this->actor, play, MTXMODE_NEW);
        }
        Gfx_SetupDL25_Opa(play->state.gfxCtx);
        Matrix_RotateXS(-0x3C72, MTXMODE_APPLY);
        SkelAnime_DrawOpa(play, this->skelAnime.skeleton, this->skelAnime.jointTable, EnSw_OverrideLimbDraw, NULL,
                          &this->actor);
    }

    for (i = 0, count = 0; i < ARRAY_COUNT(this->downCountCurrent); i++) {
        count += EnSw_DrawDamageEffects(this, play, i);
    }

    if (count != 0) {
        this->numActiveEffects += 3;
    }
}
