package com.lixar.athena.model;

import com.j256.ormlite.field.DatabaseField;
import com.lixar.athena.Athena;
import java.io.Serializable;
/**
 * Created by pzhou on 2016-05-17.
 */
public abstract class Entity implements Serializable {
    // Note:  Annotations exist for both Moshi and ORMLite.  This is ideal, it helps to avoid multiple
    // different versions the data model, and data mapper classes between them
    @DatabaseField(generatedId = true, columnName = "id")
    protected transient  int id;

    public Athena getAthena() {
        return athena;
    }

    public void setAthena(Athena athena) {
        this.athena = athena;
    }

    protected transient Athena athena;
}